# Google Drive API

The Google Drive API allows clients to access resources from Google Drive.

Docs: https://developers.google.com/workspace/drive/

## Methods

### `drive.about.get`

`drive.about.get()`

Gets information about the user, the user's Drive, and system capabilities. For more information, see [Return user info](https://developers.google.com/workspace/drive/api/guides/user-info). Required: The `fields` parameter must be set. To return the exact fields you need, see [Return specific fields](https://developers.google.com/workspace/drive/api/guides/fields-parameter).

### `drive.accessproposals.get`

`drive.accessproposals.get(file_id, proposal_id)`

Retrieves an access proposal by ID. For more information, see [Manage pending access proposals](https://developers.google.com/workspace/drive/api/guides/pending-access).

### `drive.accessproposals.list`

`drive.accessproposals.list(file_id, page_size=None, page_token=None)`

List the access proposals on a file. For more information, see [Manage pending access proposals](https://developers.google.com/workspace/drive/api/guides/pending-access). Note: Only approvers are able to list access proposals on a file. If the user isn't an approver, a 403 error is returned.

### `drive.accessproposals.resolve`

`drive.accessproposals.resolve(file_id, proposal_id, body=None)`

Approves or denies an access proposal. For more information, see [Manage pending access proposals](https://developers.google.com/workspace/drive/api/guides/pending-access).

### `drive.approvals.get`

`drive.approvals.get(approval_id, file_id)`

Gets an Approval by ID.

### `drive.approvals.list`

`drive.approvals.list(file_id, page_size=None, page_token=None)`

Lists the Approvals on a file.

### `drive.apps.get`

`drive.apps.get(app_id)`

Gets a specific app. For more information, see [Return user info](https://developers.google.com/workspace/drive/api/guides/user-info).

### `drive.apps.list`

`drive.apps.list(app_filter_extensions=None, app_filter_mime_types=None, language_code=None)`

Lists a user's installed apps. For more information, see [Return user info](https://developers.google.com/workspace/drive/api/guides/user-info).

### `drive.changes.get_start_page_token`

`drive.changes.get_start_page_token(drive_id=None, supports_all_drives=None, supports_team_drives=None, team_drive_id=None)`

Gets the starting pageToken for listing future changes. For more information, see [Retrieve changes](https://developers.google.com/workspace/drive/api/guides/manage-changes).

### `drive.changes.list`

`drive.changes.list(page_token=None, drive_id=None, include_corpus_removals=None, include_items_from_all_drives=None, include_labels=None, include_permissions_for_view=None, include_removed=None, include_team_drive_items=None, page_size=None, restrict_to_my_drive=None, spaces=None, supports_all_drives=None, supports_team_drives=None, team_drive_id=None)`

Lists the changes for a user or shared drive. For more information, see [Retrieve changes](https://developers.google.com/workspace/drive/api/guides/manage-changes).

### `drive.changes.watch`

`drive.changes.watch(page_token=None, drive_id=None, include_corpus_removals=None, include_items_from_all_drives=None, include_labels=None, include_permissions_for_view=None, include_removed=None, include_team_drive_items=None, page_size=None, restrict_to_my_drive=None, spaces=None, supports_all_drives=None, supports_team_drives=None, team_drive_id=None, body=None)`

Subscribes to changes for a user. For more information, see [Notifications for resource changes](https://developers.google.com/workspace/drive/api/guides/push).

### `drive.channels.stop`

`drive.channels.stop(body=None)`

Stops watching resources through this channel. For more information, see [Notifications for resource changes](https://developers.google.com/workspace/drive/api/guides/push).

### `drive.comments.create`

`drive.comments.create(file_id, body=None)`

Creates a comment on a file. For more information, see [Manage comments and replies](https://developers.google.com/workspace/drive/api/guides/manage-comments). Required: The `fields` parameter must be set. To return the exact fields you need, see [Return specific fields](https://developers.google.com/workspace/drive/api/guides/fields-parameter).

### `drive.comments.delete`

`drive.comments.delete(comment_id, file_id)`

Deletes a comment. For more information, see [Manage comments and replies](https://developers.google.com/workspace/drive/api/guides/manage-comments).

### `drive.comments.get`

`drive.comments.get(comment_id, file_id, include_deleted=None)`

Gets a comment by ID. For more information, see [Manage comments and replies](https://developers.google.com/workspace/drive/api/guides/manage-comments). Required: The `fields` parameter must be set. To return the exact fields you need, see [Return specific fields](https://developers.google.com/workspace/drive/api/guides/fields-parameter).

### `drive.comments.list`

`drive.comments.list(file_id, include_deleted=None, page_size=None, page_token=None, start_modified_time=None)`

Lists a file's comments. For more information, see [Manage comments and replies](https://developers.google.com/workspace/drive/api/guides/manage-comments). Required: The `fields` parameter must be set. To return the exact fields you need, see [Return specific fields](https://developers.google.com/workspace/drive/api/guides/fields-parameter).

### `drive.comments.update`

`drive.comments.update(comment_id, file_id, body=None)`

Updates a comment with patch semantics. For more information, see [Manage comments and replies](https://developers.google.com/workspace/drive/api/guides/manage-comments). Required: The `fields` parameter must be set. To return the exact fields you need, see [Return specific fields](https://developers.google.com/workspace/drive/api/guides/fields-parameter).

### `drive.drives.create`

`drive.drives.create(request_id=None, body=None)`

Creates a shared drive. For more information, see [Manage shared drives](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives).

### `drive.drives.delete`

`drive.drives.delete(drive_id, allow_item_deletion=None, use_domain_admin_access=None)`

Permanently deletes a shared drive for which the user is an `organizer`. The shared drive cannot contain any untrashed items. For more information, see [Manage shared drives](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives).

### `drive.drives.get`

`drive.drives.get(drive_id, use_domain_admin_access=None)`

Gets a shared drive's metadata by ID. For more information, see [Manage shared drives](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives).

### `drive.drives.hide`

`drive.drives.hide(drive_id)`

Hides a shared drive from the default view. For more information, see [Manage shared drives](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives).

### `drive.drives.list`

`drive.drives.list(page_size=None, page_token=None, q=None, use_domain_admin_access=None)`

 Lists the user's shared drives. This method accepts the `q` parameter, which is a search query combining one or more search terms. For more information, see the [Search for shared drives](/workspace/drive/api/guides/search-shareddrives) guide.

### `drive.drives.unhide`

`drive.drives.unhide(drive_id)`

Restores a shared drive to the default view. For more information, see [Manage shared drives](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives).

### `drive.drives.update`

`drive.drives.update(drive_id, use_domain_admin_access=None, body=None)`

Updates the metadata for a shared drive. For more information, see [Manage shared drives](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives).

### `drive.files.copy`

`drive.files.copy(file_id, enforce_single_parent=None, ignore_default_visibility=None, include_labels=None, include_permissions_for_view=None, keep_revision_forever=None, ocr_language=None, supports_all_drives=None, supports_team_drives=None, body=None)`

Creates a copy of a file and applies any requested updates with patch semantics. For more information, see [Create and manage files](https://developers.google.com/workspace/drive/api/guides/create-file).

### `drive.files.create`

`drive.files.create(enforce_single_parent=None, ignore_default_visibility=None, include_labels=None, include_permissions_for_view=None, keep_revision_forever=None, ocr_language=None, supports_all_drives=None, supports_team_drives=None, use_content_as_indexable_text=None, body=None, upload=None, upload_content_type=None)`

 Creates a file. For more information, see [Create and manage files](/workspace/drive/api/guides/create-file). This method supports an */upload* URI and accepts uploaded media with the following characteristics: - *Maximum file size:* 5,120 GB - *Accepted Media MIME types:* `*/*` (Specify a valid MIME type, rather than the literal `*/*` value. The literal `*/*` is only used to indicate that any valid MIME type can be uploaded. For more information, see [Google Workspace and Google Drive supported MIME types](/workspace/drive/api/guides/mime-types).) For more information on uploading files, see [Upload file data](/workspace/drive/api/guides/manage-uploads). Apps creating shortcuts with the `create` method must specify the MIME type `application/vnd.google-apps.shortcut`. Apps should specify a file extension in the `name` property when inserting files with the API. For example, an operation to insert a JPEG file should specify something like `"name": "cat.jpg"` in the metadata. Subsequent `GET` requests include the read-only `fileExtension` property populated with the extension originally specified in the `name` property. When a Google Drive user requests to download a file, or when the file is downloaded through the sync client, Drive builds a full filename (with extension) based on the name. In cases where the extension is missing, Drive attempts to determine the extension based on the file's MIME type.

### `drive.files.delete`

`drive.files.delete(file_id, enforce_single_parent=None, supports_all_drives=None, supports_team_drives=None)`

Permanently deletes a file owned by the user without moving it to the trash. For more information, see [Trash or delete files and folders](https://developers.google.com/workspace/drive/api/guides/delete). If the file belongs to a shared drive, the user must be an `organizer` on the parent folder. If the target is a folder, all descendants owned by the user are also deleted.

### `drive.files.download`

`drive.files.download(file_id, mime_type=None, revision_id=None)`

Downloads the content of a file. For more information, see [Download and export files](https://developers.google.com/workspace/drive/api/guides/manage-downloads). Operations are valid for 24 hours from the time of creation.

### `drive.files.empty_trash`

`drive.files.empty_trash(drive_id=None, enforce_single_parent=None)`

Permanently deletes all of the user's trashed files. For more information, see [Trash or delete files and folders](https://developers.google.com/workspace/drive/api/guides/delete).

### `drive.files.export`

`drive.files.export(file_id, mime_type=None, download=None)`

Exports a Google Workspace document to the requested MIME type and returns exported byte content. For more information, see [Download and export files](https://developers.google.com/workspace/drive/api/guides/manage-downloads). Note that the exported content is limited to 10 MB.

### `drive.files.generate_ids`

`drive.files.generate_ids(count=None, space=None, type=None)`

Generates a set of file IDs which can be provided in create or copy requests. For more information, see [Create and manage files](https://developers.google.com/workspace/drive/api/guides/create-file).

### `drive.files.get`

`drive.files.get(file_id, acknowledge_abuse=None, include_labels=None, include_permissions_for_view=None, supports_all_drives=None, supports_team_drives=None, download=None)`

 Gets a file's metadata or content by ID. For more information, see [Search for files and folders](/workspace/drive/api/guides/search-files). If you provide the URL parameter `alt=media`, then the response includes the file contents in the response body. Downloading content with `alt=media` only works if the file is stored in Drive. To download Google Docs, Sheets, and Slides use [`files.export`](/workspace/drive/api/reference/rest/v3/files/export) instead. For more information, see [Download and export files](/workspace/drive/api/guides/manage-downloads).

### `drive.files.list`

`drive.files.list(corpora=None, corpus=None, drive_id=None, include_items_from_all_drives=None, include_labels=None, include_permissions_for_view=None, include_team_drive_items=None, order_by=None, page_size=None, page_token=None, q=None, spaces=None, supports_all_drives=None, supports_team_drives=None, team_drive_id=None)`

 Lists the user's files. For more information, see [Search for files and folders](/workspace/drive/api/guides/search-files). This method accepts the `q` parameter, which is a search query combining one or more search terms. This method returns *all* files by default, including trashed files. If you don't want trashed files to appear in the list, use the `trashed=false` query parameter to remove trashed files from the results.

### `drive.files.list_labels`

`drive.files.list_labels(file_id, max_results=None, page_token=None)`

Lists the labels on a file. For more information, see [List labels on a file](https://developers.google.com/workspace/drive/api/guides/list-labels).

### `drive.files.modify_labels`

`drive.files.modify_labels(file_id, body=None)`

Modifies the set of labels applied to a file. For more information, see [Set a label field on a file](https://developers.google.com/workspace/drive/api/guides/set-label). Returns a list of the labels that were added or modified.

### `drive.files.update`

`drive.files.update(file_id, add_parents=None, enforce_single_parent=None, include_labels=None, include_permissions_for_view=None, keep_revision_forever=None, ocr_language=None, remove_parents=None, supports_all_drives=None, supports_team_drives=None, use_content_as_indexable_text=None, body=None, upload=None, upload_content_type=None)`

 Updates a file's metadata, content, or both. When calling this method, only populate fields in the request that you want to modify. When updating fields, some fields might be changed automatically, such as `modifiedDate`. This method supports patch semantics. This method supports an */upload* URI and accepts uploaded media with the following characteristics: - *Maximum file size:* 5,120 GB - *Accepted Media MIME types:* `*/*` (Specify a valid MIME type, rather than the literal `*/*` value. The literal `*/*` is only used to indicate that any valid MIME type can be uploaded. For more information, see [Google Workspace and Google Drive supported MIME types](/workspace/drive/api/guides/mime-types).) For more information on uploading files, see [Upload file data](/workspace/drive/api/guides/manage-uploads).

### `drive.files.watch`

`drive.files.watch(file_id, acknowledge_abuse=None, include_labels=None, include_permissions_for_view=None, supports_all_drives=None, supports_team_drives=None, body=None)`

Subscribes to changes to a file. For more information, see [Notifications for resource changes](https://developers.google.com/workspace/drive/api/guides/push).

### `drive.operations.get`

`drive.operations.get(name)`

Gets the latest state of a long-running operation. Clients can use this method to poll the operation result at intervals as recommended by the API service.

### `drive.permissions.create`

`drive.permissions.create(file_id, email_message=None, enforce_expansive_access=None, enforce_single_parent=None, move_to_new_owners_root=None, send_notification_email=None, supports_all_drives=None, supports_team_drives=None, transfer_ownership=None, use_domain_admin_access=None, body=None)`

Creates a permission for a file or shared drive. For more information, see [Share files, folders, and drives](https://developers.google.com/workspace/drive/api/guides/manage-sharing). **Warning:** Concurrent permissions operations on the same file aren't supported; only the last update is applied.

### `drive.permissions.delete`

`drive.permissions.delete(file_id, permission_id, enforce_expansive_access=None, supports_all_drives=None, supports_team_drives=None, use_domain_admin_access=None)`

Deletes a permission. For more information, see [Share files, folders, and drives](https://developers.google.com/workspace/drive/api/guides/manage-sharing). **Warning:** Concurrent permissions operations on the same file aren't supported; only the last update is applied.

### `drive.permissions.get`

`drive.permissions.get(file_id, permission_id, supports_all_drives=None, supports_team_drives=None, use_domain_admin_access=None)`

Gets a permission by ID. For more information, see [Share files, folders, and drives](https://developers.google.com/workspace/drive/api/guides/manage-sharing).

### `drive.permissions.list`

`drive.permissions.list(file_id, include_permissions_for_view=None, page_size=None, page_token=None, supports_all_drives=None, supports_team_drives=None, use_domain_admin_access=None)`

Lists a file's or shared drive's permissions. For more information, see [Share files, folders, and drives](https://developers.google.com/workspace/drive/api/guides/manage-sharing).

### `drive.permissions.update`

`drive.permissions.update(file_id, permission_id, enforce_expansive_access=None, remove_expiration=None, supports_all_drives=None, supports_team_drives=None, transfer_ownership=None, use_domain_admin_access=None, body=None)`

Updates a permission with patch semantics. For more information, see [Share files, folders, and drives](https://developers.google.com/workspace/drive/api/guides/manage-sharing). **Warning:** Concurrent permissions operations on the same file aren't supported; only the last update is applied.

### `drive.replies.create`

`drive.replies.create(comment_id, file_id, body=None)`

Creates a reply to a comment. For more information, see [Manage comments and replies](https://developers.google.com/workspace/drive/api/guides/manage-comments).

### `drive.replies.delete`

`drive.replies.delete(comment_id, file_id, reply_id)`

Deletes a reply. For more information, see [Manage comments and replies](https://developers.google.com/workspace/drive/api/guides/manage-comments).

### `drive.replies.get`

`drive.replies.get(comment_id, file_id, reply_id, include_deleted=None)`

Gets a reply by ID. For more information, see [Manage comments and replies](https://developers.google.com/workspace/drive/api/guides/manage-comments).

### `drive.replies.list`

`drive.replies.list(comment_id, file_id, include_deleted=None, page_size=None, page_token=None)`

Lists a comment's replies. For more information, see [Manage comments and replies](https://developers.google.com/workspace/drive/api/guides/manage-comments).

### `drive.replies.update`

`drive.replies.update(comment_id, file_id, reply_id, body=None)`

Updates a reply with patch semantics. For more information, see [Manage comments and replies](https://developers.google.com/workspace/drive/api/guides/manage-comments).

### `drive.revisions.delete`

`drive.revisions.delete(file_id, revision_id)`

Permanently deletes a file version. You can only delete revisions for files with binary content in Google Drive, like images or videos. Revisions for other files, like Google Docs or Sheets, and the last remaining file version can't be deleted. For more information, see [Manage file revisions](https://developers.google.com/drive/api/guides/manage-revisions).

### `drive.revisions.get`

`drive.revisions.get(file_id, revision_id, acknowledge_abuse=None, download=None)`

Gets a revision's metadata or content by ID. For more information, see [Manage file revisions](https://developers.google.com/workspace/drive/api/guides/manage-revisions).

### `drive.revisions.list`

`drive.revisions.list(file_id, page_size=None, page_token=None)`

Lists a file's revisions. For more information, see [Manage file revisions](https://developers.google.com/workspace/drive/api/guides/manage-revisions). **Important:** The list of revisions returned by this method might be incomplete for files with a large revision history, including frequently edited Google Docs, Sheets, and Slides. Older revisions might be omitted from the response, meaning the first revision returned may not be the oldest existing revision. The revision history visible in the Workspace editor user interface might be more complete than the list returned by the API.

### `drive.revisions.update`

`drive.revisions.update(file_id, revision_id, body=None)`

Updates a revision with patch semantics. For more information, see [Manage file revisions](https://developers.google.com/workspace/drive/api/guides/manage-revisions).

### `drive.teamdrives.create`

`drive.teamdrives.create(request_id=None, body=None)`

Deprecated: Use `drives.create` instead.

### `drive.teamdrives.delete`

`drive.teamdrives.delete(team_drive_id)`

Deprecated: Use `drives.delete` instead.

### `drive.teamdrives.get`

`drive.teamdrives.get(team_drive_id, use_domain_admin_access=None)`

Deprecated: Use `drives.get` instead.

### `drive.teamdrives.list`

`drive.teamdrives.list(page_size=None, page_token=None, q=None, use_domain_admin_access=None)`

Deprecated: Use `drives.list` instead.

### `drive.teamdrives.update`

`drive.teamdrives.update(team_drive_id, use_domain_admin_access=None, body=None)`

Deprecated: Use `drives.update` instead.
