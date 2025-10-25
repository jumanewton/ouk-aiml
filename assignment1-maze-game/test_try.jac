with entry {
    try {
        raise Exception("oops");
    } except Exception as err {
        print("caught", err);
    }
}
