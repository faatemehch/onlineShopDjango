from django.urls import path
from .views import (
    open_user_order,
    add_user_order,
    remove_order_details,
    add_single_item,
    remove_single_item,
    complete_order,
    load_cities,
    show_all_user_orders,
    show_user_order_detail,
    add_single_new_item_from_product_list,
    load_get_sent_order,
    order_user_view,
    change_to_send_order,
    send_request,
    verify
)

urlpatterns = [
    path( 'add_user_order', add_user_order, name='add_user_order' ),
    path( 'open_user_order', open_user_order, name='open_user_order' ),
    path( 'complete_order', complete_order, name='complete_order' ),
    path( 'ajax/load-cities/', load_cities, name='ajax_load_cities' ),
    path( 'ajax/load-get_sent_orders/<value>', load_get_sent_order, name='ajax_get_sent_orders' ),
    path( 'ajax/change_to_send_order/<order_id>', change_to_send_order, name='ajax_change_to_send_order' ),
    path( 'show_user_order_detail/<user_order_id>', show_user_order_detail, name='show_user_order_detail' ),
    path( 'show_all_user_orders', show_all_user_orders, name='show_all_user_orders' ),
    path( 'ajax/remove_order_details/<int:detail_id>', remove_order_details, name='ajax_remove_order_details' ),
    path( 'add_single_item/<detail_id>', add_single_item, name='add_single_item' ),
    path( 'ajax/remove_single_item/<detail_id>', remove_single_item, name='ajax_remove_single_item' ),
    path( 'add_single_new_item/<product_id>', add_single_new_item_from_product_list, name='add_single_new_item' ),
    path( 'users-order', order_user_view, name='users-order' ),
    path( 'request/', send_request, name='request' ),
    path( 'verify/<order_id>', verify, name='verify' ),
]
