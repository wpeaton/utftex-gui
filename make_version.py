# version.txt should contain two lines that looks like:
#    filevers=(3, 0, 143, 0),
#    prodvers=(3, 0, 143, 0),
# we want to increment the third number (build number)
# automatically. The first two numbers (major and minor) will be 
# incremented  by manually editing file when changes to software are big 
# enough to justify change

# pseudo code
    # open file 
    # read all lines
    # close
    # go through lines and find "filevers" and "prodvers"
    # edit those lines to increment build number
    # open file
    # write all lines
    # close 

fid = open('version.txt', 'r')
#skip first 3 lines. they are comments
for i in range(3):
    fid.readline()

# now read important line
vstring = fid.readline()
vstring = vstring.replace(' ', '')
fid.close()

left_idx = vstring.find('(') +1
right_idx = vstring.find(')')
vstring = vstring[left_idx:right_idx]

vlist = vstring.split(',')
for i, item in enumerate(vlist):
    vlist[i] = int(item)

# increment build num
vlist[2] = vlist[2]+1

major = vlist[0]
minor = vlist[1]
build = vlist[2]

verstring = '(%d, %d, %d, 0),' % (major, minor, build)
verstring2 = '%d.%d.%d.0' % (major, minor, build)

fid = open('version.txt', 'w')
fid.write('# edit major, minor manually\n')
fid.write('# build is automatically incremented. do not touch\n')
fid.write('# (major, minor, build, empty)\n')
outstring = 'filevers=' + repr(tuple(vlist))  + ','
fid.write(outstring)
fid.close()

# now we need to modify file that pyinstaller uses for setting exe version info
# read in the file
fid = open('file_version_info.txt', 'r')
flist = fid.readlines()
fid.close()

# go line by line and modify as necessary
fid = open('file_version_info.txt', 'w')
for i, line in enumerate(flist):
    if 'prodvers=' in line:
        #    prodvers=(3, 1, 115, 0),
        flist[i] = '    prodvers=%s\n' % verstring
    elif 'filevers=' in line:
        #    filevers=(3, 1, 115, 0),
        flist[i] = '    filevers=%s\n' % verstring
    elif 'FileVersion' in line:
        #        StringStruct(u'FileVersion', u'3.1.115.0'),
        flist[i] = "        StringStruct(u'FileVersion', u'%s'),\n" % verstring2
    elif 'ProductVersion' in line:
        #        StringStruct(u'ProductVersion', u'3.1.115.0'),
        flist[i] = "        StringStruct(u'ProductVersion', u'%s'),\n" % verstring2
fid.writelines(flist)
fid.close()

