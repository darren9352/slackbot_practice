import Model.Ingridient_List_Model
import Model.Receipe_Model

def show_check_menu():
    return "어떤 메뉴를 이용하시겠습니까?\n1. 시세 알아보기\n2. 계절 음식 레시피"

def display_ingridient():
    ingridient_list = Model.Ingridient_List_Model.Ingridient_List()
    ingridient_list.crawling()
    return ingridient_list.ingridient_list # return dictionary


def display_receipe(ingridient):
    receipes = Model.Receipe_Model.Receipe(ingridient)
    receipes.crawling()
    return receipes.receipe_list # return dictionary

def exit():
    return 'BYE!!!'