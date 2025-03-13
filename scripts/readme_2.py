from idiomatch import Idiomatcher


def main():
    idiomatcher = Idiomatcher.from_pretrained()  # instantiate 
    # As for a placeholder for openslot, use either: someone / something / someone's / one's 
    idioms = ["have blood on one's hands", "on one's hands"]
    idiomatcher.add_idioms(idioms)  # this will train idiomatcher to identify the given idioms
    sent = "The leaders of this war have the blood of many thousands of people on their hands."
    doc = idiomatcher.nlp(sent)
    print(idiomatcher(doc))


if __name__ == '__main__':
    main()
