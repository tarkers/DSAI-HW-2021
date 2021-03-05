
# You can write code above the if-main block.
if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='submission.csv',
                        help='output file name')
    args = parser.parse_args()

    # The following part is an example.
    # You can modify it at will.
    import pandas as pd
    df_training = pd.read_csv(args.training)
    model = Model()
    model.train(df_training)

    df_testing = pd.read_csv(args.testing)
    df_result = model.predict(df_testing)
    df_result.to_csv(args.output, index=0)
