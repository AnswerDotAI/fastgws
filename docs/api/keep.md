# Google Keep API

The Google Keep API is used in an enterprise environment to manage Google Keep content and resolve issues identified by cloud security software.

Docs: https://developers.google.com/workspace/keep/api

## Methods

### `keep.media.download`

`keep.media.download(name, mime_type=None, download=None)`

Gets an attachment. To download attachment media via REST requires the alt=media query parameter. Returns a 400 bad request error if attachment media is not available in the requested MIME type.

### `keep.notes.create`

`keep.notes.create(body=None)`

Creates a new note.

### `keep.notes.delete`

`keep.notes.delete(name)`

Deletes a note. Caller must have the `OWNER` role on the note to delete. Deleting a note removes the resource immediately and cannot be undone. Any collaborators will lose access to the note.

### `keep.notes.get`

`keep.notes.get(name)`

Gets a note.

### `keep.notes.list`

`keep.notes.list(filter=None, page_size=None, page_token=None)`

Lists notes. Every list call returns a page of results with `page_size` as the upper bound of returned items. A `page_size` of zero allows the server to choose the upper bound. The ListNotesResponse contains at most `page_size` entries. If there are more things left to list, it provides a `next_page_token` value. (Page tokens are opaque values.) To get the next page of results, copy the result's `next_page_token` into the next request's `page_token`. Repeat until the `next_page_token` returned with a page of results is empty. ListNotes return consistent results in the face of concurrent changes, or signals that it cannot with an ABORTED error.

### `keep.notes.permissions.batch_create`

`keep.notes.permissions.batch_create(parent, body=None)`

Creates one or more permissions on the note. Only permissions with the `WRITER` role may be created. If adding any permission fails, then the entire request fails and no changes are made.

### `keep.notes.permissions.batch_delete`

`keep.notes.permissions.batch_delete(parent, body=None)`

Deletes one or more permissions on the note. The specified entities will immediately lose access. A permission with the `OWNER` role can't be removed. If removing a permission fails, then the entire request fails and no changes are made. Returns a 400 bad request error if a specified permission does not exist on the note.
