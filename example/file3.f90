subroutine wav01(n,x,fun)
    implicit real*8(a-h,o-z)
    parameter (nn=9)
    dimension hx(0:n)
    pi=4.0d0*datan(1.0d0)
    fac=2.0d0*aimq01/(pi*hbar)
    if(n>=0) then
        hx(0)=1.0d0
    endif
    if(n>=1) then
        hx(1)=2.0d0*x/sqrt(2.0d0)
    endif
    if(n>=2) then
        do i=2,n
            hx(i)=x*sqrt(2.0d0/dfloat(i))*hx(i-1)-sqrt(float(i-1)/float(i))*hx(i-2)
        enddo
    endif
end