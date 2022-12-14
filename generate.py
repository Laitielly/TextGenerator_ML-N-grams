import model
from argparse import ArgumentParser


def main():
    pars = ArgumentParser()
    pars.add_argument('--model', dest='model', help='Input the directory of model')
    pars.add_argument('--prefix', dest='prefix', help='Input start of the sentence')
    pars.add_argument('--length', dest='length', help='Input the length of the sentence')
    pars.add_argument('--seed', dest='seed', help='Input the length of the sentence')

    args = pars.parse_args()
    generated = model.TextGenerator()

    print(*generated.generate(args.model, args.prefix, int(args.length), args.seed))


main()

