from bs4 import BeautifulSoup
import requests as req
import json, re
import datetime

class timetable:
    domain = "http://cabinet.sut.ru/raspisanie_all_new.php?"
    type_z = "&type_z=" # тип расписания
    facultyid = "&faculty=" # id факультета
    kurs = "&kurs=" # номер курса
    groupid = "&group=" # id группы
    year = "&schet=" # период обучения
    daysListBig=["", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


    def getYears (self) :
        link = self.domain
        soup = BeautifulSoup(req.get(link).text, 'html.parser')
        years = {'years': [] }
        try:
            for option in soup.find('form').find('select', attrs={'id':'schet'}).find_all('option'):
                if option['value'] != "0":
                    years['years'].append({'name':option.text, 'semester': option.text.split(' ')[0], 'year': option.text.split(' ')[2], 'value':option['value']})
            return years

        except:
            print("Something went wrong in getYears()!")
            return {'error':'Something wrong'}
    def getTypeTimeTable (self):
        link = self.domain
        soup = BeautifulSoup(req.get(link).text, 'html.parser')
        TypeTimeTable = {'TypeTimeTable': []}
        try:
            for option in soup.find('form').find('select', attrs={'id':'type_z'}).find_all('option'):
                if option['value'] != "0":
                    TypeTimeTable['TypeTimeTable'].append({'text':option.text, 'value':option['value']})
            return TypeTimeTable
        except:
            print("Something went wrong in getTypeTimeTable()!")
            return {'error':'Something wrong'}
    def getFacultet(self, type_z: int, schet: str):
        kurs = '0'
        facultet = {'facultet': []}
        # try:
        responce = req.post( self.domain, data={'choice':1, 'type_z': str(type_z), 'schet': str(schet), 'kurs':str(kurs)}).content.decode('utf-8').split(';')
        # except:
        #     return {'error': 523}
        # print(responce)
        try:
            if responce == ['']:
                return {'error': 404}
            else:
                for item in responce:
                    if item != "":
                        facultet['facultet'].append({'text':item.split(',')[1], 'value':item.split(',')[0]})
                return facultet
        except:
            # print("Something went wrong in getFacultet(type_z, schet)!")
            return {'error': 404}
    def getCourse (self, facultet):
        """
        Получение доступных списков курсов

        :return: list
        """
        if facultet == "56682":
            return [{"name": 1, 'value': 1}, {"name": 2, 'value': 2}]
        elif facultet == 56682:
            return [{"name": 1, 'value': 1}, {"name": 2, 'value': 2}]
        else:
            return [{"name": 1, 'value': 1}, {"name": 2, 'value': 2}, {"name": 3, 'value': 3}, {"name": 4, 'value': 4}, {"name": 5, 'value': 5}]
    def getGroups (self, facultet: int, type_z: int, schet: str, kurs: int):
        """
        Получить весь спикок групп

        :param facultet: id факультета
        :param type_z: тип расписания
        :param schet: семестр
        :param kurs: номер курса
        :return: dict
        """
        responce = req.post(self.domain, data={'faculty':str(facultet), 'choice':1, 'type_z': str(type_z), 'schet': str(schet), 'kurs':str(kurs)}).content.decode('utf-8').split(';')
        groups = {'groups': []}
        try:
            if responce == ['']:
                return {'error': 404}
            else:
                for item in responce:
                    if item != "":
                        groups['groups'].append({'group':item.split(',')[1], 'id':item.split(',')[0]})
                return groups
        except:
            # print("Something went wrong in getGroups (facultet, type_z, schet, kurs)!")
            return {'error': 500}


    def getTimeTable(self, year: str, facultetid: int, kurs: int, groupid: int, type_z: int = 1):
        """
        Получение расписания по параметрам.

        :param year: семестр
        :param type_z: тип расписания
        :param facultetid:  id факультета
        :param kurs: номер курса
        :param groupid: id курса
        :return: dict
        """
        link = self.domain + \
               self.type_z + \
               str(type_z) + \
               self.facultyid + \
               str(facultetid) + \
               self.kurs+kurs + \
               self.groupid + \
               str(groupid) + \
               self.year + \
               str(year)
        soup = BeautifulSoup(req.get(link).text, 'html.parser')
        timetableresp = {"timetable": []}
        if soup.find(string=re.compile("Занятий для выбранной группы не найдено")) is not None:
            # print({"error":404, "description":'Такого расписания нет'})
            return {"error": 404, "description":'Такого расписания нет'}
        else:
            # print(soup.find('table', attrs={'class':'simple-little-table'}))
            keys = []
            for item in soup.find('table', attrs={'class':'simple-little-table'}).find_all('th'):
                # print(item.text)
                keys.append(item.text)
                timetableresp['timetable'].append({item.text: []})
            # print(keys)
            msg = ""
            if type_z == "1":
                temp = soup.find('table', attrs={'class':'simple-little-table'}).find_all('tr')[1] #.find_all('td')[0] #.find_all('div', attrs={'class':'pair'})[0]
                # print(temp.find_all('td')[1].text == " ")
                para = []
                for item in soup.find('table', attrs={'class':'simple-little-table'}).find_all('tr'):
                    if item.find('td') is not None:
                        temp = item.find('td').text.replace(')', '').replace(' ', '').split('(')
                        para.append({'para':temp[0], 'time': temp[1]})
                # print(para)
                ipara = 0
                for table in soup.find('table', attrs={'class':'simple-little-table'}).find_all('tr'): # берем и листаем всю таблицу
                    day = 0
                    for row in table.find_all('td'): # здесь смотрим по горизонтальным столбикам (row)
                        # print("day = "+str(keys[day]))
                        if day == 0:
                            timetableresp['timetable'][day][keys[day]].append(para[ipara])
                            # print(para[ipara])
                            ipara+=1
                        if row.text != " ":
                            for column in row.find_all('div', attrs={'class':'pair'}): # здесь уже смотрим саму ячейку
                                temp = self.getInfoAboutLesson(column)
                                # print(temp[0])
                                timetableresp['timetable'][day][keys[day]].append({'lesson':temp[0], 'para':para[ipara-1]})
                        else:
                            day += 1
                            continue
                        day += 1
            # возможные поддержки расписаний. Делать я это не буду но возможно подумаю. Но расписание сессий когда-нибудь сделаю
            elif type_z == "2":
                msg = "Это расписание сессий"
                print(msg)
                return {'error':404, 'description':msg}
            elif type_z == "3":
                msg = "Это расписание факультативов"
                print(msg)
                return {'error': 404, 'description': msg}
            elif type_z == "4":
                msg = "Это расписание сессий для заочников"
                print(msg)
                return {'error': 404, 'description': msg}
            elif type_z == "5":
                msg = "Это расписание ГИА"
                print(msg)
                return {'error': 404, 'description': msg}
            elif type_z == "6":
                msg = "Это расписание канфиренций и прочего"
                print(msg)
                return {'error': 404, 'description': msg}
            elif type_z == "9":
                msg = "Это расписание контроля занятий"
                print(msg)
                return {'error': 404, 'description': msg}
            else:
                msg = "Хз что это. Куда ты опять попал?!!!???! И почему это сработало??!?!?!"
                print(msg)
                return {'error': 404, 'description': msg}
        return timetableresp['timetable']

    def getInfoAboutLesson(self, lesson): # ожидается тэг <div class="pair" weekday="2" pair="2"> с его содержимым
        """
        Парсер предмета

        :param lesson: Предмет
        :return: dict
        """
        predmet = {'predmet': []}
        typeLesson = {'typeLesson': []}
        studyWeeks = {'studyWeeks':[]}
        teachers = {'teachers': []}
        lectureHall = {'lectureHall': []}
        try:
            predmet['predmet'].append(str(lesson.span.strong.text))
        except:
            predmet['predmet'].append({'error':404, 'description': 'Do not have lesson name'})
        try:
            typeLesson['typeLesson'].append(lesson.small.find('span', attrs={'class': 'type'}).text.replace('(', '').replace(')', ''))
        except:
            typeLesson['typeLesson'].append({'error':404, 'description':'Do not have type lesson'})
        try:
            temp = lesson.small.find('span', attrs={'class': 'weeks'}).text.replace('(', '').replace(')', '').replace(' ', '').split(',')
            for hall in temp:
                studyWeeks['studyWeeks'].append(hall)
        except:
            studyWeeks['studyWeeks'].append({'error':404, 'description':'Do not have study weeks'})
        try:
            temp = lesson.i.find('span', attrs={"class": "teacher"})['title'].split('; ')
            for teacher in temp:
                if teacher != "":
                    teachers['teachers'].append(teacher)
        except:
            teachers['teachers'].append({'error':404, 'description':'Do not have teacher'})
        try:
            temp = lesson.find('span', attrs={'class': 'aud'}).text.replace(' ', '').replace('ауд.:', '').split(';')
            # print(len(temp))
            if len(temp) > 1:
                lectureHall['lectureHall'].append({'aud':temp[0], 'building': temp[1]})
            else:
                lectureHall['lectureHall'].append(temp[0])
        except:
            lectureHall['lectureHall'].append({'error': 404, 'description':'Do not have lecture hall'})
        # data = {'data': []}
        # data['data'].append()
        data = {
            'data': [
                {
                    'predmet': predmet['predmet'],
                    'studyWeeks':studyWeeks['studyWeeks'],
                    'teachers':teachers['teachers'],
                    'lectureHall':lectureHall['lectureHall']
                }
            ]
        }
        return data['data']

    def getEdWeek(self):
        """
        Получение номера учебной недели

        :return: int
        """
        yyear = datetime.date.today().year
        today = datetime.datetime.now()
        then = datetime.datetime(yyear-1, 9, 1)
        edweek = round((((today - then).days/7)+1))
        return edweek

    def curseOnCurrentWeek(self, parsedWeeks: list):
        """
        Проверка на то есть ли сегодня эта пара или нет

        :param weeks: список спаршенных номеров недель
        :return: Bool
        """
        edWeek = self.getEdWeek()
        for week in parsedWeeks:
            if int(week) == edWeek:
                return True
        return False

    def parseWeekNumber(self, weeks: list):
        """
        парсер номеров недель

        :param weeks: список не спаршенных недель
        :return: list
        """
        parsedWeeks = []
        for week in weeks:
            weekparsed = week.replace('*', '').replace("н", '')
            parsedWeeks.append(weekparsed)
        return parsedWeeks

    def getToDayTimeTable(self, year: str, facultetid: int, kurs: int, groupid: int, type_z: int = 1, weekDay: int = None):
        """

        :param year: семестр
        :param type_z: тип расписания
        :param facultetid:  id факультета
        :param kurs: номер курса
        :param groupid: id курса
        :return:
        """
        date = datetime.datetime.now()
        if weekDay == None or weekDay == 0:
            nowWeekDay = date.weekday()+1
        elif weekDay >= 7:
          return {"error": 404 }
        else:
            nowWeekDay = weekDay

        tt = self.getTimeTable(year=year, facultetid=facultetid, kurs=kurs, groupid=groupid, type_z=type_z)
        days = self.daysListBig
        toDayCurse = []
        for item in tt[nowWeekDay][days[nowWeekDay]]:
            weeks = item['lesson']['studyWeeks']
            parsedWeeks = self.parseWeekNumber(weeks)
            if self.curseOnCurrentWeek(parsedWeeks):
                toDayCurse.append(item)

        return toDayCurse


# tt = timetable()
# print(tt.getToDayTimeTable(year="205.2021/2", type_z='1', facultetid="50554", kurs='3', groupid='53954', weekDay= 0))
# print(str(tt.getTimeTable("205.2021/2", '1', "50554", '3', '53954')).replace("'", '"'))
# print(tt.getGroups(50554, 1, "205.2021/2", 3)) # получение списка групп
# print(tt.getCourse(50554)) # получение количество курсов
# print(tt.getYears()) # получение список годов
# print(tt.getFacultet(1, "205.2021/2")) # получение факультетов
