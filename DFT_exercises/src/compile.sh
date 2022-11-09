echo '-----------------------------------------------'
echo ' Creating the compilation parameters.'

cat <<eof  >param8.h
      parameter (mx=18,my=18,mz=18,mc=10,mv=mx*my*mz,mq=4*mv,mw=300)
      parameter (meven=5,modd=5)
eof
echo ' Done!'
echo '-----------------------------------------------'
echo 'Compiling nil8!'
echo '-----------------------------------------------'
gfortran -O3 -o nil8.exe nil8.f &> nil8.diag
echo '-----------------------------------------------'
echo 'Compiling ev8!'
echo '-----------------------------------------------'
gfortran -O3 -o ev8.exe ev8.f &> ev8.diag
echo 'Done!'

