from math import sqrt

def main():
    # RMSE
    with open("test_data_actual.txt") as f:
        with open("test_preds.txt") as f2:
            counter = 0
            average_error = 0.0
            for l1, l2 in zip(f, f2):
                first = float(l1)
                sec = float(l2)
                counter += 1
                average_error += ((sec - first)**2)
            print(sqrt(average_error/counter))
            

if __name__ == '__main__':
    main()
    