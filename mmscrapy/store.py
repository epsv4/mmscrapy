import sqlalchemy
import os

def find():
    # for i,j,k in os.walk("C:\\Users\\libra\\PycharmProjects"):
    for i,j,k in os.walk("E:\PycharmProjects"):
        for f in k:
            if not f.endswith("py"):
                continue
            with open(os.path.join(i, f)) as fd:
                try:
                    for line in fd:
                        if line.find("sqlalchemy") >= 0:
                            print(i, f)
                            break
                except:
                    pass

if __name__ == "__main__":
    find()