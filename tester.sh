#!/bin/bash

# Set the directory containing the input files
input_dir="./test_files"

# Set the directory containing the expected output files
expected_output_dir="./expected_files"

output_dir="./output_files"

diff_dir="./diff_files"

# Set the path to the program to be tested
program_path="python3 program.py"

# Iterate over all the .txt files in the input directory
for input_file in ${input_dir}/*.txt
do
    # Get the name of the file without the path or extension
    input_name=$(basename ${input_file} .txt)

    # Set the path to the corresponding expected output file
    expected_output_file="${expected_output_dir}/${input_name}.txt"

    # Run the program with the input file and capture its output in a temporary file
    #output=$( ${program_path} < ${input_file} )
    ${program_path} < ${input_file} > ${output_dir}/${input_name}.txt
    #echo ${output}

    #echo ${output} > ${output_dir}/${input_name}.txt

    # Compare the program output with the expected output file
    diff ${output_dir}/${input_name}.txt "${expected_output_file}" > ${diff_dir}/${input_name}.txt

    # Check the exit status of the diff command to determine whether the output matches the expected output
    if [ $? -eq 0 ]; then
        echo "Test ${input_name}: PASSED"
    else
        echo "Test ${input_name}: FAILED"
    fi
done