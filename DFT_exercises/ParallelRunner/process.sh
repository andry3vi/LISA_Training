#-------------------------------------------------------------------------------
# Example script for EV8.
#
# This script executes the following steps:
#
# 1) Compile nil8 & ev8 for computations for the selected isotopes.
# 2) Run nil8 to create an initial guess on a file fort.12
# 3) Run ev8 with fort.12 to get a result.
#-------------------------------------------------------------------------------

#Compiler to use
compiler=gfortran

clear

#-------------------------------- Settings --------------------------------#
srcdir="../src"
neutron_numbers=("126" "128" "130" "132" "134" "136" "138" "140" "142" "144" "146")
# neutron_numbers=( "126" "128" "130" "132" "134" "136" "138" "140" "142" "144" "146" "148" "150" "152" "154" "156" "158" "160" "162" "164" "166" "168" "170" "172" "174" "178" )
# neutron_numbers=("120" "122" "124" "148" "150" "152" "154" "156" "158" "160" "162" "164" "166") 
# neutron_numbers=("168" "170" "172" "174" "176" "178" "180" "182" "184" "186" "188" "190")
iterations="0500"
type="oblate"

echo '------------------------------------------------------------------------------------------
███╗   ███╗██╗   ██╗██╗  ████████╗██╗██████╗ ██╗   ██╗███╗   ██╗███╗   ██╗███████╗██████╗ 
████╗ ████║██║   ██║██║  ╚══██╔══╝██║██╔══██╗██║   ██║████╗  ██║████╗  ██║██╔════╝██╔══██╗
██╔████╔██║██║   ██║██║     ██║   ██║██████╔╝██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██║╚██╔╝██║██║   ██║██║     ██║   ██║██╔══██╗██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║██║  ██║╚██████╔╝██║ ╚████║██║ ╚████║███████╗██║  ██║
╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                                                                          
------------------------------------------------------------------------------------------'
echo 'initial settings'
echo "iterations -> $iterations" 
echo "type       -> $type" 

echo '--------------------------------'
echo 'Creating working directories'
basedir=$PWD
srcdir=$basedir/$srcdir
workdir="$PWD/run_$(date +"%FT%H%M%S")"
echo $workdir
executables=$workdir/executables
inputs=$workdir/inputs
outputs=$workdir/outputs

mkdir -p $executables
mkdir -p $inputs
mkdir -p $outputs
echo ' Done!'

echo '--------------------------------'
echo 'Copying executables'
cp $srcdir/*.f $executables
echo 'Done!'

echo '-----------------------------------------------'
echo 'Creating the compilation parameters.'
cat << eof > $executables/param8.h
      parameter (mx=18,my=18,mz=18,mc=10,mv=mx*my*mz,mq=4*mv,mw=300)
      parameter (meven=5,modd=5)
eof
echo 'Done!'

echo '-----------------------------------------------'
echo 'Compiling nil8!'
#Compiling NIL8
$compiler -o $executables/xnil8 $executables/nil8.f &> $executables/nil8.diag
# echo 'Compiled!'
echo 'Done!'

echo '-----------------------------------------------'
echo 'Creating runtime NIL8 parameters for each isotope:'
for nn in ${neutron_numbers[@]}; do
      echo " -> $nn neutrons <- "
      cp $srcdir/nil8.$type.template.data $inputs/$nn.nil8.$type.data
      sed -i "s/nnn/$nn/" $inputs/$nn.nil8.$type.data
done

echo 'Done!'

echo '-----------------------------------------------'
echo 'Running NIL8 for each isotope'
for nn in ${neutron_numbers[@]}; do
      mkdir "$workdir/tmp_$nn"
      cd "$workdir/tmp_$nn"
      $executables/xnil8 < $inputs/$nn.nil8.$type.data > $outputs/$nn.nil8.$type.out &
      cd $workdir
done
wait

echo 'Done!'

echo '-----------------------------------------------'
echo 'Moving fort.13 for each isotope'
for nn in ${neutron_numbers[@]}; do
      cd "$workdir/tmp_$nn"
      mv fort.13 fort.12
      cd $workdir
done
echo 'Done!'

echo '-----------------------------------------------'
echo 'Compiling EV8'
$compiler -O3 -o $executables/xev8 $executables/ev8.f &> $executables/ev8.diag
echo 'Done!'

echo '-----------------------------------------------'
echo 'Creating runtime ev8 data for each isotope:'
for nn in ${neutron_numbers[@]}; do
      echo " -> $nn neutrons <- "
      cp $srcdir/EV8.template.data $inputs/$nn.ev8.data
      sed -i "s/nnn/$nn/" $inputs/$nn.ev8.data
      sed -i "s/iiii/$iterations/" $inputs/$nn.ev8.data
done

echo '-----------------------------------------------'
echo 'Running EV8'
for nn in ${neutron_numbers[@]}; do
      cd "$workdir/tmp_$nn"
      time $executables/xev8 < $inputs/$nn.ev8.data > $outputs/$nn.ev8.$type.out &
      cd $workdir
done
wait

echo '-----------------------------------------------'
echo 'cleaning tmp files' 
rm -r tmp*