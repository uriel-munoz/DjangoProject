import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "college.settings")

import django
django.setup()

from django.contrib.auth.models import User

from store.models import Product


def populate():
    password="123"
    student = add_student("Daniel", "Gopar", "dgopar@csumb.edu",password)

    add_product("Toaster", "Brand new toaster from Google", 15, student)
    add_product("Laptop", "Hardly used HP laptop", 200, student)

    student = add_student("Uriel", "Last-name", "uriel@csumb.edu",password)

    add_product("Candy", "Newest candy on the block", 1, student)
    add_product("Math Book", "CST205 book", 200.34, student)

    student = add_student("Daniel", "Ibarra", "ibarra@csumb.edu",password)

    add_product("HTML Book", "Great beginner book for HTML", 20, student)
    add_product("Mac laptop", "Used Mac laptop", 500, student)


def print_db():
    # Print what we have done
    for s in User.objects.all():
        for p in Product.objects.filter(student=s):
            print("- {} - {}".format(str(s), str(p)))


def add_product(product, description, price, student):
    p = Product.objects.get_or_create(product=product, description=description,
                                      price=price, student=student)[0]
    p.save()
    return p


def add_student(first_name, last_name, email,newpassword):
    s = User.objects.get_or_create(first_name=first_name, last_name=last_name,
                                   email=email, username=email)[0]
    s.set_password(newpassword);
    s.save()
    return s

if __name__ == '__main__':
    print("Starting to populate DB...\n")
    populate()
    print_db()
