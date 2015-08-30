# -*- coding: utf-8 -*-

from rdg import generator

def main():
    width = height = 36
    g = generator.Generator(width, height)
    g.generate()
    
    for i in range(0, height):
        for j in range(0, width):
            if g.map[i][j] == 0:
                    print ' ',
            else:
                print '*',
        print ''

if __name__ == '__main__':
    main()