
#####################################################################
# CONFIGURATIONS
#####################################################################
test_input = r'D:\OneDrive\PythonWorkspace\booleanFormulas\train_input_01-07-2017-15-36-53'
test_output = r'D:\OneDrive\PythonWorkspace\booleanFormulas\train_output_01-07-2017-15-36-53'
predictions = r'D:\OneDrive\PythonWorkspace\booleanFormulas\predict'

filter_output = r'D:\OneDrive\PythonWorkspace\booleanFormulas\filter_out'

# filter options
correct_prediction = True

input_line = 'a'
counter = 0

with open(test_input,'r') as f_test_in,\
    open(test_output,'r') as f_test_out,\
    open(predictions,'r') as f_prediction,\
    open(filter_output,'w') as f_filter:
    while input_line != '':
        input_line = f_test_in.readline()
        output_line = f_test_out.readline()
        predict_line = f_prediction.readline()

        if output_line == predict_line:
            f_filter.write(input_line + predict_line)
            counter += 1
    f_filter.write('total_count=' + str(counter))
