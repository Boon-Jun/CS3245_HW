import os

os.system("python generateNewTrainTestCorrectData.py")
os.system("python build_test_LM.py -b BJInput.train.txt -t BJInput.test.txt -o output_file")
os.system("python eval.py output_file BJInput.correct.txt")
