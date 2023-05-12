def outer_splitter(fpy, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size):
    fpy.write("\n")
    fpy.write(f"outer_splitter = {outersplitter}(")
    if outersplitter == 'LeaveOneOut':
        fpy.write(")\n")
    elif outersplitter == 'GroupShuffleSplit':
        if test_size > train_size: 
            fpy.write(f"n_splits={n_splits}, test_size={test_size}, random_state={cv_rd})\n")
        else:
            fpy.write(f"n_splits={n_splits}, train_size={train_size}, random_state={cv_rd})\n")
    elif outersplitter == 'RepeatedStratifiedKFold':
        fpy.write(f"n_splits={n_splits}, n_repeats={n_repeat}, random_state={cv_rd})\n")