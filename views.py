from danni_framework.templator import render
from patterns.creational_patterns import Engine
from patterns.logger_singleton import Logger

site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, requests):
        return '200 OK', render('index.html', date=requests.get('date', None), objects_list=site.categories)


class Programs:
    def __call__(self, requests):
        return '200 OK', render('programs.html', date=requests.get('date', None))


class Contacts:
    def __call__(self, requests):
        return '200 OK', render('contacts.html', date=requests.get('date', None))


class CoursesList:
    def __call__(self, requests):
        logger.log('course_list')
        try:
            category = site.find_category_by_id(int(requests['request_params']['id']))
            return '200 OK', render('courses-list.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


class CreateCourse:
    category_id = -1

    def __call__(self, requests):
        if requests['method'] == 'POST':
            data = requests['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('web', name, category)
                site.courses.append(course)

            return '200 OK', render('courses-list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(requests['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create-course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'
            except ValueError:
                return '200 OK', 'No categories have been added yet'


class CreateCategory:
    def __call__(self, requests):
        if requests['method'] == 'POST':
            data = requests['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create-category.html',
                                    categories=categories)


class CategoryList:
    def __call__(self, requests):
        logger.log('categories list')
        return '200 OK', render('category-list.html',
                                objects_list=site.categories)


class CopyCourse:
    def __call__(self, requests):
        request_params = requests['request_params']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('courses-list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name)

        except KeyError:
            return '200 OK', 'No courses have been added yet'
