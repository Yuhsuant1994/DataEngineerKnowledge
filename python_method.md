# Python methods

In Python, the three main types of methods that can be defined within a class are:

* **Instance methods:** These are the regular object-oriented methods, which can modify the state of an instance and also the class.

* **Class methods:** These are methods which are bound to the class and not the instance of the class. They can modify the class state that would be shared amongst all instances.

* **Static methods:** These are methods that don't operate on an instance and don't have access to the rest of the class unless explicitly provided.

---

## Instance Methods:

These are the most common type of methods. They always take self as the first argument, which is a reference to the instance of the class. Instance methods can access and modify instance data (attributes set on self).

Example:

```
class MyClass:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

instance = MyClass(5)
print(instance.get_value())  # Prints "5"
```


## Class Methods:

These are methods that are bound to the class and not the instance of the class. They can't access or modify instance data (unless an instance is explicitly provided), but they can access and modify class level data. They are defined using the @classmethod decorator.

```
class MyClass:
    value = 10

    @classmethod
    def get_value(cls):
        return cls.value

print(MyClass.get_value())  # Prints "10"
```
### how class method can access and modify class level data
```
class MyClass:
    # Class-level data
    count = 0

    def __init__(self):
        # Each time an instance is created, increase the count
        MyClass.count += 1
        # If count has reached 5, reset it to 0
        if MyClass.count > 5:
            MyClass.count = 0

    @classmethod
    def get_count(cls):
        # This class method accesses class-level data
        return cls.count

# Create some instances
for _ in range(10):
    a = MyClass()
    print(MyClass.get_count())  # Will print 1, 2, 3, 4, 5, 0, 1, 2, 3, 4
```

## Static Methods:

These are methods that belong to a class rather than an instance of the class, and don't implicitly pass any reference to either the class or the instance. They cannot modify the state of the class or the instance, but can access it if explicitly provided. They are defined using the @staticmethod decorator.

object no need to be created

```

class MyClass:
    @staticmethod
    def say_hello():
        print("Hello, world!")

MyClass.say_hello()  # Prints "Hello, world!"
```


A static method in Python cannot directly create or modify instance variables (those defined with self) or class variables (those defined directly within the class body). This is because static methods do not have access to self (the instance) or cls (the class).

However, a static method can certainly create local variables within its own scope, like any other function. It can also return these local variables to the caller, and it can operate on values that are passed to it as parameters.
