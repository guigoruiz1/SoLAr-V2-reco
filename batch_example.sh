# Loop through all files matching the pattern in the specified directory
for file in ../Monte\ Carlo/singlecube_cry_hit_*
do
  # Print the current file name
  echo $file
  
  # Extract the numbers after 'hit_' and before '.root' using sed to get the output folder
  label=$(echo $file | sed -n 's/.*hit_\([0-9]*\)\.root/\1/p')
  
  # Run the reconstruction script simulating dead areas and dh set to 30
  ./reconstruction.py $file -d -p force_dh=30
  
  # Run the analysis script on the output folder
  ./analysis.py $label -d -s
  
  # Run the reconstruction script again without simulating dead areas
  ./reconstruction.py $file -p force_dh=30
  
  # Run the analysis script again on the output folder
  ./analysis.py $label -s
done