import model
import argparse


def main():
    pars = argparse.ArgumentParser()
    pars.add_argument('--input-dir', dest='filename', help='Input the directory of file')
    pars.add_argument('--model', dest='model', help='Input the directory of model')

    args = pars.parse_args()
    prepare = model.TextGenerator()

    filename = args.filename
    text = ''

    if filename is None:
        text = input('Please, input your text:\n')
    else:
        try:
            f = open(filename, 'r', encoding='utf-8')
        except IOError as e:
            print(u'Could not open the file, please, try again')
            exit()
        else:
            for i in f:
                text += i.lower()
            f.close()

    prepare.fit(text, args.model)


main()
