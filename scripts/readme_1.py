from idiomatch import Idiomatcher


def main():
    sent = "The floodgates will remain opened for a host of new lawsuits."  # a usecase of *open the floodgates*
    idiomatcher = Idiomatcher.from_pretrained()  # this will take approx 50 seconds.
    doc = idiomatcher.nlp(sent)  # use and only use the nlp model that comes with the matcher 
    print(idiomatcher(doc))  # identify the idiom in the sentence


if __name__ == '__main__':
    main()
