import re,sys,argparse

parser = argparse.ArgumentParser(description='Convert fixed source FORTRAN 77 code to indented modern free form Fortran 90 code')

parser.add_argument('file',metavar='PATH',type=str,help='Name of the input file')
parser.add_argument('-o',metavar='PATH',type=str,help='Name of the output file')
parser.add_argument('-maxcol',metavar='MAXCOL',type=int,default=120,help='Maximum allowed column')
parser.add_argument('-indent',metavar='INDENT',type=int,default=4,help='Length of indentation of each labels')
parser.add_argument('-keepndo',default=False,action='store_true',help="Keep numbered do blocks")
parser.add_argument('-keepblank',default=False,action='store_true',help='Keep blank lines')
parser.add_argument('-progstate',default=False,action='store_true',help='Insert a `program` statement at the top')


args = parser.parse_args()

fileName = args.file
outFileName = args.o if args.o else fileName.replace('.f','.f90') 
MAXCOL = args.maxcol                # maximum column after which to wrap
INDENT = args.indent                  # indentation for each code block
CONVERT_NUMBERED_DO = not args.keepndo  # convert numbered do loop ?
REMOVE_BLANK = not args.keepblank         # remove unwanted blank lines?
PROGRAM_STATEMENT = not args.progstate    # Inserts `program` statement at the beginning


def splitIntoLines(txt,offset):
    # warps a long line in multi line
    txt = txt.strip()

    isOMP, isComment,toStart,toEnd = False,False,'',' &'
    if txt.startswith('!$omp'):   # openmp line
        isOMP = True
        toSplit = '(,)'
        toStart = '!$omp& '
    elif txt.startswith('!'):    # commented line
        isComment = True
        toSplit = '( )'
        toStart = '! '
        toEnd   = ''
    else:                        #usual code line
        toSplit = '(\*|\+|,)'

    txt = re.split(toSplit,txt)

    tt = ['']
    for i in txt:
        if len(tt[-1]) + len(i) > MAXCOL-offset-3: # 3 for the continuation symbol
            tt[-1]+=toEnd
            tt.append(i)
        else:
            tt[-1]+=i
    tt[1:] = [toStart+i for i in tt[1:]]
    return '\n'.join([ ' '*offset+i for i in tt  ])



with open(fileName) as f:
    code = f.read().lower().split('\n')


#this is ugly
if PROGRAM_STATEMENT : code.insert(0,'program test')  


formatGroups={}  # collect format groups to replace inside the write statements
for i in range(len(code)):
    m = re.search('\s+(\d+)\s+format(\(.*\))',code[i])
    if m:
        formatGroups[m.group(1)] = m.group(2)
        code[i] = ''

for i in range(len(code)-1,0,-1):
    if not code[i].strip(): continue 

    comment = True if code[i].strip().startswith('!') else False

    if code[i] and code[i][0] in 'cC*':  # commented line
        code[i] ='!'+ code[i][1:]
        comment = True


    if code[i][5:6] != ' ' and not comment:   # continuation line, merge it with previous line
        prevLine = code[i-1]
        ll = prevLine.find('!')
        if ll!=-1:
            prevLine = prevLine[:prevLine.find('!')]
        curLine  = code[i][6:]
        code[i-1]= prevLine.rstrip() + curLine.strip()
        code[i] = ''


    if code[i].strip().startswith('!$omp$'): # continuation line for openmp
        code[i-1] =code[i-1].rstrip() + code[i].replace('!$omp$', '').strip()
        code[i] = ''
        comment = False
    
    m = re.search(  'write\([0-9* ]+,(\d+)\)',code[i]) # replace write formats
    if m:
        form = formatGroups[ m.group(1)]
        code[i] = re.sub('write\(([0-9* ]+),(\d+)\)' , r'write(\1,"{}")'.format(form), code[i])


    # remove return end before stop
    if code[i].strip().lower() in ['return', 'stop'] and code[i+1].strip().lower()=='end':
        code[i] = ''

    if comment or not CONVERT_NUMBERED_DO : continue
    # numbered do blocks
    m = re.search('\s+do\s+(\d+)', code[i])
    if m:  # found one numbered do
        doLabel = m.group(1)
        doLine  = m .group().strip()
        
        ll=1 # check back if there's other do loop like with the same label
        for j in range(i-1,0,-1):
            if doLine in code[j]:
                ll+=1
                code[j] = code[j].replace(doLine , 'do') 
            elif code[j].strip()=='end':  # stop check if going outside of funcion or subroutine
                break
        
        for j in range(i+1,len(code)):
            m = re.search('\s+(\d+)\s+(\w+)', code[j])
            if m:
                label = m.group(1)
                if label == doLabel:
                    # remove number from do and insert a enddo at the end
                    code[i] = code[i].replace(doLine , 'do') 
                    for _ in range(ll) : code.insert(j+1,'enddo')
                    # remove the continue/label statements
                    if m.group(2)=="continue":
                        code[j] = ''
                    else:
                        code[j] = re.sub('^\s+(\d+)\s+','', code[j])
                    break


if REMOVE_BLANK: code = list(filter(None, [i.strip() for i in code]))


# indent the code
# Increase indentation if encountered do,if,else
# decrease indentation if encountered end
# reset indentation if encountered subroutine/function/program  #<-- fix this
currentIndent = 0
for i in range(len(code)):
    line = code[i].strip()
    if line.startswith('end') or line.startswith('else'):  
        currentIndent -=INDENT

    code[i] = currentIndent*' '+code[i]

    if len(code[i]) > MAXCOL:
        code[i] = splitIntoLines(code[i], currentIndent)

    # increase
    if (line.startswith('do') and not line.startswith('double'))or \
       line.startswith('else') or \
       (line.startswith('if') and line.endswith('then')):
        currentIndent +=INDENT

    elif line.startswith('subroutine') or line.startswith('function') :
        currentIndent = INDENT
        code[i] = '\n\n'+code[i].strip()

    elif line.startswith('program'):
        currentIndent = INDENT
        


# removes old style logical operator
txt = '\n'.join(code)
txt = re.sub('\.ge\.', ">=", txt)
txt = re.sub('\.le\.', "<=", txt)
txt = re.sub('\.eq\.', "==", txt)
txt = re.sub('\.ne\.', "/=", txt)
txt = re.sub('\.gt\.', ">", txt)
txt = re.sub('\.lt\.', "<", txt)



with open(outFileName, 'w') as f:
    f.write(txt)
print('File saved as {}'.format(outFileName))