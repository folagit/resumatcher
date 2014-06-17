#!/usr/bin/env python

def throws():
    raise RuntimeError('this is the error message')

def main():
    print "----- good part 1 ----"
    throws()
    print "----- good part 2-----"

if __name__ == '__main__':
    main()
