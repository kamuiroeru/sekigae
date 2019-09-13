# Sekigae Program
For Sekigae Program

## Requirements
- python >= 3.6 ( Use f-strings )

## Install
shell
```shell script
pip install sekigae
```

## Shell Command Usage
### Simple usage

shell
```shell script
# 45 Students to 6 rows.
sekigae 45 6
```

output
```text
             FRONT
-------------------------------
| 23 | 21 | 25 |  1 |  8 | 45 |
-------------------------------
| 18 | 29 | 44 |  4 | 20 | 42 |
-------------------------------
|  2 | 10 | 35 | 30 | 15 | 31 |
-------------------------------
| 37 |  6 | 27 | 40 | 36 | 11 |
-------------------------------
| 16 | 39 |  5 | 14 |  3 | 17 |
-------------------------------
| 28 | 34 |  9 | 13 | 19 | 43 |
-------------------------------
| 32 | 26 |  7 | 12 | 41 | 22 |
-------------------------------
| 38 | 33 | 24 |
```

### Edit top label
shell
```shell script
# set tag as "WhiteBoard"
sekigae 25 6 -t WhiteBoard
```

output
```text
          WhiteBoard
-------------------------------
| 24 | 21 |  7 | 17 | 13 | 15 |
-------------------------------
|  9 |  5 | 10 | 25 | 22 | 16 |
-------------------------------
| 19 | 18 | 20 |  4 |  1 |  6 |
-------------------------------
| 11 |  8 |  3 | 23 | 12 |  2 |
-------------------------------
| 14 |
```

### Read CSV
out.csv
```csv
9,12,6,10,8
5,11,2,4,7
3,1
```

shell
```shell script
# choose csv (ignore simple use options)
sekigae 45 6 --csv out.csv
```

output
```text
          FRONT
--------------------------
|  9 | 12 |  6 | 10 |  8 |
--------------------------
|  5 | 11 |  2 |  4 |  7 |
--------------------------
|  3 |  1 |
```

### Write CSV
shell
```shell script
# write table to "test.csv"
sekigae 11 4 -o test.csv
```

output
```text
        FRONT
---------------------
| 11 |  6 | 10 |  1 |
---------------------
|  8 |  5 |  2 |  4 |
---------------------
|  9 |  3 |  7 |
csv wrote
```

test.csv
```csv
11,6,10,1
8,5,2,4
9,3,7
```

### fix student specific place
shell
```shell script
# format is "row:col:number"
# fix '7' to 1st row 2nd col and fix '9' 1st row 4th col
sekigae 11 4 -s 1:2:7,1:4:9
```

output
```text
        FRONT
---------------------
|  6 |  7 |  1 |  9 |
---------------------
|  3 |  8 |  2 | 10 |
---------------------
|  4 | 11 |  5 |

        FRONT        
---------------------
|  5 |  7 |  8 |  9 |
---------------------
|  6 | 11 | 10 |  2 |
---------------------
|  1 |  3 |  4 |

        FRONT        
---------------------
|  8 |  7 | 11 |  9 |
---------------------
| 10 |  6 |  2 |  4 |
---------------------
|  3 |  5 |  1 |
```

`7` is fixed 1st row 2nd col.
`9` is fixed 1st row 4th col.

### Pipeline
#### Pipeline input
out.csv
```text
10,12,3,5,6
11,4,9,1,13
7,8,2
```
```shell script
cat out.csv | sekigae
```
output
```text
          FRONT
--------------------------
| 10 | 12 |  3 |  5 |  6 |
--------------------------
| 11 |  4 |  9 |  1 | 13 |
--------------------------
|  7 |  8 |  2 |
```

#### Pipeline output
```shell script
sekigae 13 5 -f | awk '{ if (gsub(/,/, " ")) print }'
```
output
```text
8 5 7 10 12
11 6 3 4 1
13 2 9
```