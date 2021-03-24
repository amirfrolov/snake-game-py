class Table:
    def __init__(self, val=None):
        self.data = dict()
        if val != None:
            self.insert(val)

# Insert method to create nodes
    def insert(self, val):
        if val != None:
            if type(val) == Table:
                for i in val.valuesList():
                    self.insert(i)
            elif type(val) == list:
                for i in val:
                    self.insert(i)
            else:
                self.data[val] = None
        else:
            pass

# findval method to compare the value with nodes
    def find(self, val):
        return val in self.data

# remove value
    def remove(self, val):
        if val != None:
            if type(val) == Table:
                for i in val.valuesList():
                    self.remove(i)
            elif type(val) == list:
                for i in val:
                    self.remove(i)
            else:
                self.data.pop(val, None)
        else:
            pass

    def list(self):
        return list(self.data.keys())

    def __iadd__(self, other):
        self.insert(other)
        return self

    def __isub__(self, other):
        self.remove(other)
        return self

    def __add__(self, other):
        result = Table(self)
        print(result.valuesList())
        result += other
        return result

    def __sub__(self, other):
        result = Table(self)
        result -= other
        return result


def main():
    #raise Exception('spam', 'eggs')
    root = Table([1, 2, 5]) + Table([8, 9])
    print(root.valuesList())
    root.insert(6)
    root.insert(14)
    root.insert([3, 1, 2])
    print(root.valuesList())
    # root.remove(3)
    print(root.find(7))
    print(root.find(14))
    print(root.find(3))


if __name__ == "__main__":
    main()
