from fastapi.testclient import TestClient
from .conftest import client,test_book_super_admin_user, test_book_super_admin_header


from src.config import setup_logger
logger = setup_logger()


BOOK_TITLE_UNDER_TEST  = "http test title"

def test_create_book_http(client:TestClient, 
                               test_book_super_admin_user:dict, 
                               test_book_super_admin_header:dict
):
    json_data = {
        "title":BOOK_TITLE_UNDER_TEST,
        "category":"http category",
        "description":"http description"
    }
    response = client.post('/books/create-book',
                          json=json_data,
                           headers=test_book_super_admin_header)
    
    assert response.status_code==200
    data = response.json()
    assert data['title'] == 'http test title'

    
def test_update_book_http(client:TestClient, 
                               test_book_super_admin_user:dict, 
                               test_book_super_admin_header:dict
):
    #get book by id and title

    response = client.get(f'/books/read-book/{BOOK_TITLE_UNDER_TEST}',
                                headers=test_book_super_admin_header)
    
    assert response.status_code==200
    assert response.json()['title']==BOOK_TITLE_UNDER_TEST

    data = response.json()
    
    id_response = client.get(f'/books/{data["id"]}',
                             headers=test_book_super_admin_header)
    
    assert id_response.status_code==200
    assert id_response.json()['title'] == BOOK_TITLE_UNDER_TEST

    new_data = {
        'category':'updated http test category'
    }
    update_response = client.put(f'/books/{data["id"]}',
                                 json=new_data,
                                 headers=test_book_super_admin_header)
    
    assert update_response.status_code == 200

    updated_data = update_response.json()

    assert updated_data['category']== 'updated http test category'

def test_delete_book(client:TestClient,
                    test_book_super_admin_user:dict, 
                    test_book_super_admin_header:dict
):
    response = client.get(f'/books/read-book/{BOOK_TITLE_UNDER_TEST}',
                                headers=test_book_super_admin_header)
    
    data = response.json()

    deleted_response = client.delete(f'/books/{data["id"]}/delete',
                                     headers=test_book_super_admin_header)

    assert deleted_response.status_code == 200
    assert deleted_response.json()['detail']=="1" 