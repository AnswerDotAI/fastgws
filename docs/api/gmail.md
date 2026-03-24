# Gmail API

The Gmail API lets you view and manage Gmail mailbox data like threads, messages, and labels.

Docs: https://developers.google.com/workspace/gmail/api/

## Methods

### `gmail.users.drafts.create`

`gmail.users.drafts.create(user_id, body=None, upload=None, upload_content_type=None)`

Creates a new draft with the `DRAFT` label.

### `gmail.users.drafts.delete`

`gmail.users.drafts.delete(id, user_id)`

Immediately and permanently deletes the specified draft. Does not simply trash it.

### `gmail.users.drafts.get`

`gmail.users.drafts.get(id, user_id, format=None)`

Gets the specified draft.

### `gmail.users.drafts.list`

`gmail.users.drafts.list(user_id, include_spam_trash=None, max_results=None, page_token=None, q=None)`

Lists the drafts in the user's mailbox.

### `gmail.users.drafts.send`

`gmail.users.drafts.send(user_id, body=None, upload=None, upload_content_type=None)`

Sends the specified, existing draft to the recipients in the `To`, `Cc`, and `Bcc` headers.

### `gmail.users.drafts.update`

`gmail.users.drafts.update(id, user_id, body=None, upload=None, upload_content_type=None)`

Replaces a draft's content.

### `gmail.users.get_profile`

`gmail.users.get_profile(user_id)`

Gets the current user's Gmail profile.

### `gmail.users.history.list`

`gmail.users.history.list(user_id, history_types=None, label_id=None, max_results=None, page_token=None, start_history_id=None)`

Lists the history of all changes to the given mailbox. History results are returned in chronological order (increasing `historyId`).

### `gmail.users.labels.create`

`gmail.users.labels.create(user_id, body=None)`

Creates a new label.

### `gmail.users.labels.delete`

`gmail.users.labels.delete(id, user_id)`

Immediately and permanently deletes the specified label and removes it from any messages and threads that it is applied to.

### `gmail.users.labels.get`

`gmail.users.labels.get(id, user_id)`

Gets the specified label.

### `gmail.users.labels.list`

`gmail.users.labels.list(user_id)`

Lists all labels in the user's mailbox.

### `gmail.users.labels.patch`

`gmail.users.labels.patch(id, user_id, body=None)`

Patch the specified label.

### `gmail.users.labels.update`

`gmail.users.labels.update(id, user_id, body=None)`

Updates the specified label.

### `gmail.users.messages.attachments.get`

`gmail.users.messages.attachments.get(id, message_id, user_id)`

Gets the specified message attachment.

### `gmail.users.messages.batch_delete`

`gmail.users.messages.batch_delete(user_id, body=None)`

Deletes many messages by message ID. Provides no guarantees that messages were not already deleted or even existed at all.

### `gmail.users.messages.batch_modify`

`gmail.users.messages.batch_modify(user_id, body=None)`

Modifies the labels on the specified messages.

### `gmail.users.messages.delete`

`gmail.users.messages.delete(id, user_id)`

Immediately and permanently deletes the specified message. This operation cannot be undone. Prefer `messages.trash` instead.

### `gmail.users.messages.get`

`gmail.users.messages.get(id, user_id, format=None, metadata_headers=None)`

Gets the specified message.

### `gmail.users.messages.import_`

`gmail.users.messages.import_(user_id, deleted=None, internal_date_source=None, never_mark_spam=None, process_for_calendar=None, body=None, upload=None, upload_content_type=None)`

Imports a message into only this user's mailbox, with standard email delivery scanning and classification similar to receiving via SMTP. This method doesn't perform SPF checks, so it might not work for some spam messages, such as those attempting to perform domain spoofing. This method does not send a message. Note that the maximum size of the message is 150MB.

### `gmail.users.messages.insert`

`gmail.users.messages.insert(user_id, deleted=None, internal_date_source=None, body=None, upload=None, upload_content_type=None)`

Directly inserts a message into only this user's mailbox similar to `IMAP APPEND`, bypassing most scanning and classification. Does not send a message.

### `gmail.users.messages.list`

`gmail.users.messages.list(user_id, include_spam_trash=None, label_ids=None, max_results=None, page_token=None, q=None)`

Lists the messages in the user's mailbox. For example usage, see [List Gmail messages](https://developers.google.com/workspace/gmail/api/guides/list-messages).

### `gmail.users.messages.modify`

`gmail.users.messages.modify(id, user_id, body=None)`

Modifies the labels on the specified message.

### `gmail.users.messages.send`

`gmail.users.messages.send(user_id, body=None, upload=None, upload_content_type=None)`

Sends the specified message to the recipients in the `To`, `Cc`, and `Bcc` headers. For example usage, see [Sending email](https://developers.google.com/workspace/gmail/api/guides/sending).

### `gmail.users.messages.trash`

`gmail.users.messages.trash(id, user_id)`

Moves the specified message to the trash.

### `gmail.users.messages.untrash`

`gmail.users.messages.untrash(id, user_id)`

Removes the specified message from the trash.

### `gmail.users.settings.cse.identities.create`

`gmail.users.settings.cse.identities.create(user_id, body=None)`

Creates and configures a client-side encryption identity that's authorized to send mail from the user account. Google publishes the S/MIME certificate to a shared domain-wide directory so that people within a Google Workspace organization can encrypt and send mail to the identity. For administrators managing identities and keypairs for users in their organization, requests require authorization with a [service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) that has [domain-wide delegation authority](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority) to impersonate users with the `https://www.googleapis.com/auth/gmail.settings.basic` scope. For users managing their own identities and keypairs, requests require [hardware key encryption](https://support.google.com/a/answer/14153163) turned on and configured.

### `gmail.users.settings.cse.identities.delete`

`gmail.users.settings.cse.identities.delete(cse_email_address, user_id)`

Deletes a client-side encryption identity. The authenticated user can no longer use the identity to send encrypted messages. You cannot restore the identity after you delete it. Instead, use the CreateCseIdentity method to create another identity with the same configuration. For administrators managing identities and keypairs for users in their organization, requests require authorization with a [service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) that has [domain-wide delegation authority](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority) to impersonate users with the `https://www.googleapis.com/auth/gmail.settings.basic` scope. For users managing their own identities and keypairs, requests require [hardware key encryption](https://support.google.com/a/answer/14153163) turned on and configured.

### `gmail.users.settings.cse.identities.get`

`gmail.users.settings.cse.identities.get(cse_email_address, user_id)`

Retrieves a client-side encryption identity configuration. For administrators managing identities and keypairs for users in their organization, requests require authorization with a [service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) that has [domain-wide delegation authority](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority) to impersonate users with the `https://www.googleapis.com/auth/gmail.settings.basic` scope. For users managing their own identities and keypairs, requests require [hardware key encryption](https://support.google.com/a/answer/14153163) turned on and configured.

### `gmail.users.settings.cse.identities.list`

`gmail.users.settings.cse.identities.list(user_id, page_size=None, page_token=None)`

Lists the client-side encrypted identities for an authenticated user. For administrators managing identities and keypairs for users in their organization, requests require authorization with a [service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) that has [domain-wide delegation authority](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority) to impersonate users with the `https://www.googleapis.com/auth/gmail.settings.basic` scope. For users managing their own identities and keypairs, requests require [hardware key encryption](https://support.google.com/a/answer/14153163) turned on and configured.

### `gmail.users.settings.cse.identities.patch`

`gmail.users.settings.cse.identities.patch(email_address, user_id, body=None)`

Associates a different key pair with an existing client-side encryption identity. The updated key pair must validate against Google's [S/MIME certificate profiles](https://support.google.com/a/answer/7300887). For administrators managing identities and keypairs for users in their organization, requests require authorization with a [service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) that has [domain-wide delegation authority](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority) to impersonate users with the `https://www.googleapis.com/auth/gmail.settings.basic` scope. For users managing their own identities and keypairs, requests require [hardware key encryption](https://support.google.com/a/answer/14153163) turned on and configured.

### `gmail.users.settings.cse.keypairs.create`

`gmail.users.settings.cse.keypairs.create(user_id, body=None)`

Creates and uploads a client-side encryption S/MIME public key certificate chain and private key metadata for the authenticated user. For administrators managing identities and keypairs for users in their organization, requests require authorization with a [service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) that has [domain-wide delegation authority](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority) to impersonate users with the `https://www.googleapis.com/auth/gmail.settings.basic` scope. For users managing their own identities and keypairs, requests require [hardware key encryption](https://support.google.com/a/answer/14153163) turned on and configured.

### `gmail.users.settings.cse.keypairs.disable`

`gmail.users.settings.cse.keypairs.disable(key_pair_id, user_id, body=None)`

Turns off a client-side encryption key pair. The authenticated user can no longer use the key pair to decrypt incoming CSE message texts or sign outgoing CSE mail. To regain access, use the EnableCseKeyPair to turn on the key pair. After 30 days, you can permanently delete the key pair by using the ObliterateCseKeyPair method. For administrators managing identities and keypairs for users in their organization, requests require authorization with a [service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) that has [domain-wide delegation authority](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority) to impersonate users with the `https://www.googleapis.com/auth/gmail.settings.basic` scope. For users managing their own identities and keypairs, requests require [hardware key encryption](https://support.google.com/a/answer/14153163) turned on and configured.

### `gmail.users.settings.cse.keypairs.enable`

`gmail.users.settings.cse.keypairs.enable(key_pair_id, user_id, body=None)`

Turns on a client-side encryption key pair that was turned off. The key pair becomes active again for any associated client-side encryption identities. For administrators managing identities and keypairs for users in their organization, requests require authorization with a [service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) that has [domain-wide delegation authority](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority) to impersonate users with the `https://www.googleapis.com/auth/gmail.settings.basic` scope. For users managing their own identities and keypairs, requests require [hardware key encryption](https://support.google.com/a/answer/14153163) turned on and configured.

### `gmail.users.settings.cse.keypairs.get`

`gmail.users.settings.cse.keypairs.get(key_pair_id, user_id)`

Retrieves an existing client-side encryption key pair. For administrators managing identities and keypairs for users in their organization, requests require authorization with a [service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) that has [domain-wide delegation authority](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority) to impersonate users with the `https://www.googleapis.com/auth/gmail.settings.basic` scope. For users managing their own identities and keypairs, requests require [hardware key encryption](https://support.google.com/a/answer/14153163) turned on and configured.

### `gmail.users.settings.cse.keypairs.list`

`gmail.users.settings.cse.keypairs.list(user_id, page_size=None, page_token=None)`

Lists client-side encryption key pairs for an authenticated user. For administrators managing identities and keypairs for users in their organization, requests require authorization with a [service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) that has [domain-wide delegation authority](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority) to impersonate users with the `https://www.googleapis.com/auth/gmail.settings.basic` scope. For users managing their own identities and keypairs, requests require [hardware key encryption](https://support.google.com/a/answer/14153163) turned on and configured.

### `gmail.users.settings.cse.keypairs.obliterate`

`gmail.users.settings.cse.keypairs.obliterate(key_pair_id, user_id, body=None)`

Deletes a client-side encryption key pair permanently and immediately. You can only permanently delete key pairs that have been turned off for more than 30 days. To turn off a key pair, use the DisableCseKeyPair method. Gmail can't restore or decrypt any messages that were encrypted by an obliterated key. Authenticated users and Google Workspace administrators lose access to reading the encrypted messages. For administrators managing identities and keypairs for users in their organization, requests require authorization with a [service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) that has [domain-wide delegation authority](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority) to impersonate users with the `https://www.googleapis.com/auth/gmail.settings.basic` scope. For users managing their own identities and keypairs, requests require [hardware key encryption](https://support.google.com/a/answer/14153163) turned on and configured.

### `gmail.users.settings.delegates.create`

`gmail.users.settings.delegates.create(user_id, body=None)`

Adds a delegate with its verification status set directly to `accepted`, without sending any verification email. The delegate user must be a member of the same Google Workspace organization as the delegator user. Gmail imposes limitations on the number of delegates and delegators each user in a Google Workspace organization can have. These limits depend on your organization, but in general each user can have up to 25 delegates and up to 10 delegators. Note that a delegate user must be referred to by their primary email address, and not an email alias. Also note that when a new delegate is created, there may be up to a one minute delay before the new delegate is available for use. This method is only available to service account clients that have been delegated domain-wide authority.

### `gmail.users.settings.delegates.delete`

`gmail.users.settings.delegates.delete(delegate_email, user_id)`

Removes the specified delegate (which can be of any verification status), and revokes any verification that may have been required for using it. Note that a delegate user must be referred to by their primary email address, and not an email alias. This method is only available to service account clients that have been delegated domain-wide authority.

### `gmail.users.settings.delegates.get`

`gmail.users.settings.delegates.get(delegate_email, user_id)`

Gets the specified delegate. Note that a delegate user must be referred to by their primary email address, and not an email alias. This method is only available to service account clients that have been delegated domain-wide authority.

### `gmail.users.settings.delegates.list`

`gmail.users.settings.delegates.list(user_id)`

Lists the delegates for the specified account. This method is only available to service account clients that have been delegated domain-wide authority.

### `gmail.users.settings.filters.create`

`gmail.users.settings.filters.create(user_id, body=None)`

Creates a filter. Note: you can only create a maximum of 1,000 filters.

### `gmail.users.settings.filters.delete`

`gmail.users.settings.filters.delete(id, user_id)`

Immediately and permanently deletes the specified filter.

### `gmail.users.settings.filters.get`

`gmail.users.settings.filters.get(id, user_id)`

Gets a filter.

### `gmail.users.settings.filters.list`

`gmail.users.settings.filters.list(user_id)`

Lists the message filters of a Gmail user.

### `gmail.users.settings.forwarding_addresses.create`

`gmail.users.settings.forwarding_addresses.create(user_id, body=None)`

Creates a forwarding address. If ownership verification is required, a message will be sent to the recipient and the resource's verification status will be set to `pending`; otherwise, the resource will be created with verification status set to `accepted`. This method is only available to service account clients that have been delegated domain-wide authority.

### `gmail.users.settings.forwarding_addresses.delete`

`gmail.users.settings.forwarding_addresses.delete(forwarding_email, user_id)`

Deletes the specified forwarding address and revokes any verification that may have been required. This method is only available to service account clients that have been delegated domain-wide authority.

### `gmail.users.settings.forwarding_addresses.get`

`gmail.users.settings.forwarding_addresses.get(forwarding_email, user_id)`

Gets the specified forwarding address.

### `gmail.users.settings.forwarding_addresses.list`

`gmail.users.settings.forwarding_addresses.list(user_id)`

Lists the forwarding addresses for the specified account.

### `gmail.users.settings.get_auto_forwarding`

`gmail.users.settings.get_auto_forwarding(user_id)`

Gets the auto-forwarding setting for the specified account.

### `gmail.users.settings.get_imap`

`gmail.users.settings.get_imap(user_id)`

Gets IMAP settings.

### `gmail.users.settings.get_language`

`gmail.users.settings.get_language(user_id)`

Gets language settings.

### `gmail.users.settings.get_pop`

`gmail.users.settings.get_pop(user_id)`

Gets POP settings.

### `gmail.users.settings.get_vacation`

`gmail.users.settings.get_vacation(user_id)`

Gets vacation responder settings.

### `gmail.users.settings.send_as.create`

`gmail.users.settings.send_as.create(user_id, body=None)`

Creates a custom "from" send-as alias. If an SMTP MSA is specified, Gmail will attempt to connect to the SMTP service to validate the configuration before creating the alias. If ownership verification is required for the alias, a message will be sent to the email address and the resource's verification status will be set to `pending`; otherwise, the resource will be created with verification status set to `accepted`. If a signature is provided, Gmail will sanitize the HTML before saving it with the alias. This method is only available to service account clients that have been delegated domain-wide authority.

### `gmail.users.settings.send_as.delete`

`gmail.users.settings.send_as.delete(send_as_email, user_id)`

Deletes the specified send-as alias. Revokes any verification that may have been required for using it. This method is only available to service account clients that have been delegated domain-wide authority.

### `gmail.users.settings.send_as.get`

`gmail.users.settings.send_as.get(send_as_email, user_id)`

Gets the specified send-as alias. Fails with an HTTP 404 error if the specified address is not a member of the collection.

### `gmail.users.settings.send_as.list`

`gmail.users.settings.send_as.list(user_id)`

Lists the send-as aliases for the specified account. The result includes the primary send-as address associated with the account as well as any custom "from" aliases.

### `gmail.users.settings.send_as.patch`

`gmail.users.settings.send_as.patch(send_as_email, user_id, body=None)`

Patch the specified send-as alias.

### `gmail.users.settings.send_as.smime_info.delete`

`gmail.users.settings.send_as.smime_info.delete(id, send_as_email, user_id)`

Deletes the specified S/MIME config for the specified send-as alias.

### `gmail.users.settings.send_as.smime_info.get`

`gmail.users.settings.send_as.smime_info.get(id, send_as_email, user_id)`

Gets the specified S/MIME config for the specified send-as alias.

### `gmail.users.settings.send_as.smime_info.insert`

`gmail.users.settings.send_as.smime_info.insert(send_as_email, user_id, body=None)`

Insert (upload) the given S/MIME config for the specified send-as alias. Note that pkcs12 format is required for the key.

### `gmail.users.settings.send_as.smime_info.list`

`gmail.users.settings.send_as.smime_info.list(send_as_email, user_id)`

Lists S/MIME configs for the specified send-as alias.

### `gmail.users.settings.send_as.smime_info.set_default`

`gmail.users.settings.send_as.smime_info.set_default(id, send_as_email, user_id)`

Sets the default S/MIME config for the specified send-as alias.

### `gmail.users.settings.send_as.update`

`gmail.users.settings.send_as.update(send_as_email, user_id, body=None)`

Updates a send-as alias. If a signature is provided, Gmail will sanitize the HTML before saving it with the alias. Addresses other than the primary address for the account can only be updated by service account clients that have been delegated domain-wide authority.

### `gmail.users.settings.send_as.verify`

`gmail.users.settings.send_as.verify(send_as_email, user_id)`

Sends a verification email to the specified send-as alias address. The verification status must be `pending`. This method is only available to service account clients that have been delegated domain-wide authority.

### `gmail.users.settings.update_auto_forwarding`

`gmail.users.settings.update_auto_forwarding(user_id, body=None)`

Updates the auto-forwarding setting for the specified account. A verified forwarding address must be specified when auto-forwarding is enabled. This method is only available to service account clients that have been delegated domain-wide authority.

### `gmail.users.settings.update_imap`

`gmail.users.settings.update_imap(user_id, body=None)`

Updates IMAP settings.

### `gmail.users.settings.update_language`

`gmail.users.settings.update_language(user_id, body=None)`

Updates language settings. If successful, the return object contains the `displayLanguage` that was saved for the user, which may differ from the value passed into the request. This is because the requested `displayLanguage` may not be directly supported by Gmail but have a close variant that is, and so the variant may be chosen and saved instead.

### `gmail.users.settings.update_pop`

`gmail.users.settings.update_pop(user_id, body=None)`

Updates POP settings.

### `gmail.users.settings.update_vacation`

`gmail.users.settings.update_vacation(user_id, body=None)`

Updates vacation responder settings.

### `gmail.users.stop`

`gmail.users.stop(user_id)`

Stop receiving push notifications for the given user mailbox.

### `gmail.users.threads.delete`

`gmail.users.threads.delete(id, user_id)`

Immediately and permanently deletes the specified thread. Any messages that belong to the thread are also deleted. This operation cannot be undone. Prefer `threads.trash` instead.

### `gmail.users.threads.get`

`gmail.users.threads.get(id, user_id, format=None, metadata_headers=None)`

Gets the specified thread.

### `gmail.users.threads.list`

`gmail.users.threads.list(user_id, include_spam_trash=None, label_ids=None, max_results=None, page_token=None, q=None)`

Lists the threads in the user's mailbox.

### `gmail.users.threads.modify`

`gmail.users.threads.modify(id, user_id, body=None)`

Modifies the labels applied to the thread. This applies to all messages in the thread.

### `gmail.users.threads.trash`

`gmail.users.threads.trash(id, user_id)`

Moves the specified thread to the trash. Any messages that belong to the thread are also moved to the trash.

### `gmail.users.threads.untrash`

`gmail.users.threads.untrash(id, user_id)`

Removes the specified thread from the trash. Any messages that belong to the thread are also removed from the trash.

### `gmail.users.watch`

`gmail.users.watch(user_id, body=None)`

Set up or update a push notification watch on the given user mailbox.
