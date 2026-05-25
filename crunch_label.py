

def give_crunch_label(label, crunch_label_by=5):
    if crunch_label_by is None:
        return label
    if type(label) == str:
        return give_crunch_label_single(label, crunch_label_by)
    elif type(label) == dict:
        new_dict = {}
        for key, item in label.items():
            new_dict[key] = give_crunch_label_single(item, crunch_label_by)
        print(new_dict)
        return new_dict
    elif type(label) == list:
        new_list = []
        for s in label:
            new_list.append(give_crunch_label_single(s, crunch_label_by))
        return new_list


def give_crunch_label_single(label, crunch_label_by):
    label_list = label.split(" ")

    count = 0
    new_label_list = []
    for word in label_list:

        count += len(word)
        if count > crunch_label_by:
            word = word + "<br>"
            count = 0
        else:
            word += " "
        new_label_list.append(word)
        count += 1

    return ("").join(new_label_list)


if __name__ == "__main__":
    label = "1 - stimme überhaupt nicht zu"
    s = give_crunch_label(label, crunch_label_by=8)
    print(s)