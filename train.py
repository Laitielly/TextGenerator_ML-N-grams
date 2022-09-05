import model
import argparse


def main():
    pars = argparse.ArgumentParser()
    pars.add_argument('--input-dir', dest='filename', help='Input the directory of file')
    pars.add_argument('--model', dest='model', help='Input the directory of model')

    args = pars.parse_args()
    prepare = model.TextGenerator()

    prepare.fit(args.model, args.filename)


main()
