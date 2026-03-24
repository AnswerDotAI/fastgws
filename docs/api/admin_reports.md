# Admin SDK API

Admin SDK lets administrators of enterprise domains to view and manage resources like user, groups etc. It also provides audit and usage reports of domain.

Docs: https://developers.google.com/workspace/admin/

## Methods

### `admin_reports.activities.list`

`admin_reports.activities.list(application_name, user_key, actor_ip_address=None, application_info_filter=None, customer_id=None, end_time=None, event_name=None, filters=None, group_id_filter=None, max_results=None, network_info_filter=None, org_unit_id=None, page_token=None, resource_details_filter=None, start_time=None, status_filter=None)`

Retrieves a list of activities for a specific customer's account and application such as the Admin console application or the Google Drive application. For more information, see the guides for administrator and Google Drive activity reports. For more information about the activity report's parameters, see the activity parameters reference guides. 

### `admin_reports.activities.watch`

`admin_reports.activities.watch(application_name, user_key, actor_ip_address=None, customer_id=None, end_time=None, event_name=None, filters=None, group_id_filter=None, max_results=None, org_unit_id=None, page_token=None, start_time=None, body=None)`

Start receiving notifications for account activities. For more information, see Receiving Push Notifications.

### `admin_reports.channels.stop`

`admin_reports.channels.stop(body=None)`

Stop watching resources through this channel.

### `admin_reports.customer_usage_reports.get`

`admin_reports.customer_usage_reports.get(date, customer_id=None, page_token=None, parameters=None)`

Retrieves a report which is a collection of properties and statistics for a specific customer's account. For more information, see the Customers Usage Report guide. For more information about the customer report's parameters, see the Customers Usage parameters reference guides. 

### `admin_reports.entity_usage_reports.get`

`admin_reports.entity_usage_reports.get(date, entity_key, entity_type, customer_id=None, filters=None, max_results=None, page_token=None, parameters=None)`

Retrieves a report which is a collection of properties and statistics for entities used by users within the account. For more information, see the Entities Usage Report guide. For more information about the entities report's parameters, see the Entities Usage parameters reference guides.

### `admin_reports.user_usage_report.get`

`admin_reports.user_usage_report.get(date, user_key, customer_id=None, filters=None, group_id_filter=None, max_results=None, org_unit_id=None, page_token=None, parameters=None)`

Retrieves a report which is a collection of properties and statistics for a set of users with the account. For more information, see the User Usage Report guide. For more information about the user report's parameters, see the Users Usage parameters reference guides.
