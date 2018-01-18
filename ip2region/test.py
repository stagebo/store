from ip2region import ip2Region
import sys
import sys
type = sys.getfilesystemencoding()

dbFile = 'data/ip2region.db'
searcher = ip2Region.Ip2Region(dbFile);
method = 1
line = '39.106.157.61'
if method == 1:
    data = searcher.btreeSearch(line)
elif method == 2:
    data = searcher.binarySearch(line)
else:
    data = searcher.memorySearch(line)

print(data)
print(data["region"].decode('utf-8'))