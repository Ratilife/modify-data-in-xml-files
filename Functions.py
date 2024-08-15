import os
import threading
#import xml.etree.ElementTree as ET
from lxml import etree as ET



class Functions:

    def processing_xml(self, path_to_the_file, data_for_the_substitution, processed_files, old_value):
        """
        Функция для обработки одного XML-файла.

        Args:
            path_to_the_file (str): Путь к XML-файлу.
            data_for_the_substitution (dict): Словарь с данными для замены.
            processed_files (list): Список обработанных XML-файлов.
            old_value (str): Старое значение, которое требуется заменить.

        Returns:
            None.

        Обзор функций:
            - Обрабатывает один XML-файл.
            - Разбирает содержимое XML.
            - Применяет заданные текстовые замены на основе предоставленного словаря.
            - Сохраняет измененный XML-файл.
            - Обрабатывает ошибки при разборе и сохранении XML-файла.
            - Добавляет имя файла в список обработанных файлов, если обработка прошла успешно.
        """

        errors_occurred = False

        # Проверка существования файла
        if not os.path.exists(path_to_the_file):
            print(f"Файл '{path_to_the_file}' не найден.")
            return

        try:
            # Попытка разбора XML-файла и получение пространства имен по умолчанию
            parser = ET.XMLParser(remove_blank_text=True)
            tree = ET.parse(path_to_the_file, parser)
            root = tree.getroot()
        except ET.ParseError as e:
             # Обработка ошибок при разборе XML-файла
            print(f"Ошибка при парсинге XML-файла '{path_to_the_file}': {e}")
            errors_occurred = True
            return

        if not errors_occurred:
             # Применение замен из словаря к элементам XML
            for key, value in data_for_the_substitution.items():
                # for element in root.iter():
                #     # Проверяем, совпадает ли значение атрибута с old_value
                #     if element.get(key) == old_value:
                #         # Меняем значение атрибута
                #         element.set(key, value)
                if key in root.attrib:
                    if root.get(key) == old_value:
                        root.attrib[key]=value

            try:
                # Сохранение измененного XML-файла
                tree.write(path_to_the_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

            except Exception as e:
                 # Обработка ошибок при сохранении XML-файла
                print(f"Ошибка при сохранении XML-файла '{path_to_the_file}': {e}")
            # Добавить обработанный файл в список
            processed_files.append(path_to_the_file)



    def generate_report(self, processed_files, path_to_report, data_for_the_substitution, path_to_folder, old_value):
        """
        Функция для формирования отчета.

        Args:
            processed_files: Список обработанных XML-файлов.
            path_to_report: Путь к файлу отчета.
            path_to_folder: Путь к папке с данными

        Returns:
            None.
        Обзор функций:
            Создает отчет, подробно описывающий результаты обработки.
            Перечисляет обработанные файлы, внесенные изменения и их исходные пути.
        """
        try:
            with open(path_to_report, "w", encoding="utf-8") as report_file:
                for file in processed_files:
                    report_file.write(f"Имя файла: {file}\n")
                    report_file.write("Изменения:\n")
                    for key, value in data_for_the_substitution.items():
                        report_file.write(f"    {old_value} -> {value}\n")
                    report_file.write(f"Путь к файлу: {os.path.join(path_to_folder, file)}\n\n")

        except IOError as e:
            print(f"Ошибка при записи отчета в файл '{path_to_report}': {e}")


    def generate_report_does_not_work(self, processed_files, data_for_the_substitution, path_to_folder):
        """
        Функция для формирования отчета.

        Args:
            processed_files: Список обработанных XML-файлов.
            data_for_the_substitution: Словарь с данными для замены.
            path_to_folder: Путь к папке с данными.

        Returns:
            str: Строка с отчетом.

        Обзор функций:
            Создает отчет, подробно описывающий результаты обработки.
            Перечисляет обработанные файлы, внесенные изменения и их исходные пути.
        """
        report = ""  # Инициализируем пустую строку для формирования отчета

        for file in processed_files:
            report += f"Имя файла: {file}\n"
            report += "Изменения:\n"
            for key, value in data_for_the_substitution.items():
                report += f"    {key} -> {value}\n"
            report += f"Путь к файлу: {os.path.join(path_to_folder, file)}\n\n"

        return report

    def start(self, Path_to_folder, data_for_the_substitution, path_to_report, old_value):
        """ Главная функция.

        начало процессса обработки файлов. Обходит файлы и помещает их в потоки.

        Аргументы:
        Path_to_folder (str): Путь к папке, содержащей файлы для обработки.
        data_for_the_substitution (dict): Словарь с данными для замены в XML файлах. {"version": "2.9"}
        path_to_report (str): Путь к файлу отчета.

        Обзор функций:
             - Инициирует процесс обработки.
             - Перечисляет файлы в указанной папке и её подпапках.
             - Создает потоки для многопроцессорной обработки XML-файлов.
             - Запускает и ожидает завершения потоков.
             - Создает отчет с обработанным списком файлов.
        """
        # Создаем список, который должен содержать имена (или полные пути) XML-файлов, успешно обработанных функцией start
        processed_files = []

        # Создаем список для хранения потоков
        streams = []
        # Рекурсивно обходим все файлы в указанной папке и её подпапках
        for root, dirs, files in os.walk(Path_to_folder):
            # root - текущая директория
            # dirs - список поддиректорий
            # files - список файлов в текущей директории
            for file in files:
                # Проверяем, что файл имеет расширение .xml
                if file.endswith(".xml"):
                    # Создаем поток для обработки каждого XML-файла
                    path_to_the_file = os.path.join(root, file)
                    stream = threading.Thread(target=self.processing_xml,
                                              args=(path_to_the_file,
                                                    data_for_the_substitution, processed_files, old_value))
                    streams.append(stream)   # Добавляем поток в список потоков
                    stream.start()           # Запускаем поток

        # Ожидаем завершения всех потоков
        for stream in streams:
            stream.join()

        # После обработки всех файлов создайте отчет с обработанным списком
        self.generate_report(processed_files,path_to_report ,data_for_the_substitution, Path_to_folder, old_value)

        # Где-то в вашем коде после получения отчета:
        #report_text = self.generate_report(processed_files, data_for_the_substitution, Path_to_folder)

    #Функционал сравнения файлов

    # Функция для рекурсивного сравнения элементов
    def compare_elements(self, elem1, elem2, path="", output_file=None):
        # Сравниваем теги элементов
        if elem1.tag != elem2.tag:
            output_file.write(f"Разные теги на пути: {path}\n")
        # Сравниваем атрибуты
        if elem1.attrib != elem2.attrib:
            output_file.write(f"Различные атрибуты на пути: {path}\n")
        # Сравниваем текстовое содержимое
        if elem1.text != elem2.text:
            output_file.write(f"Различное текстовое содержимое в пути: {path}\n")

        # Сравниваем дочерние элементы
        for child1, child2 in zip(elem1, elem2):
            self.compare_elements(child1, child2, path + "/" + child1.tag, output_file)

    def compare_xml_files(self, file1, file2, output_file_name):
        # Парсим XML-файлы
        tree1 = ET.parse(file1)
        tree2 = ET.parse(file2)

        # Получаем корневые элементы
        root1 = tree1.getroot()
        root2 = tree2.getroot()

        with open(output_file_name, "w") as output_file:
            try:
                # Начинаем сравнивать корневые элементы
                self.compare_elements(root1, root2, output_file=output_file)
                output_file.write("Различий не обнаружено. Сравниваемые файлы похожи.")
            except Exception as e:
                output_file.write(f"Во время сравнения произошла ошибка: {str(e)}")





