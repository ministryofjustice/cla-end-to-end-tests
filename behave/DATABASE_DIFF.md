## Expected Database Changes


This readme attempts to explain why there are differences between an upgrade branch and the master version of cla_backend before LGA-1773. 

If you see anything that is not explained below, then this should be queried.

Some of these changes are to do with time differences between the runs and other are because there is no ordering to the way in which results are stored. So if there is more than one row of data to add to a table, these rows can be added in a different order and so will "look" different in the target database. 

Examples are given below.


### summary.log
 There will always be a summary table, use this for a high level comparison

### django_sessions.log

This table contains details of the session and this will always be different from run to run. Just check to make sure that there is nothing ontoward.

Please add any known differences to this as we proceed.

### timer.log

This table records when the timer (which calculates how long a user has been working on a case) stops. These will be different because the tests are run on one branch and then the next.

### django_migrations.log

This table lists all the migrations that exist and the time at which they were applied. As the tests are run on one branch and then the next, these application times will be different.
There will also be some additional migrations for the upgrades. These should be checked and the reason for the change understood. They should either be additions you have made or ones made as part of the upgrade.

### cla_provider_providerpreallocation.log

Providers are allocated from a particular category. This is a random allocation. Check that the providers allocated are from the same category. In this case check that the `category_id` of both providers (in `cla_provider_providerallocation`) is the same. 

### cla_eventlog_log.log
Not sure if this should be here - need to check...

### legalaid_personaldetails.log
In the tests an eligibility check can be associated with several `legalaid_personaldetails` entries. It can be for `you`, your 'partner' or for a `thirdparty`. 

There is no way of knowing which order these entries will be created in the `legalaid_personaldetails` table. This means that they will not normally have the same id in the link tables.

Elena Fisher is `you` and a user called Nathan Drake is a `thirdparty` for a particular `legalaid_eligibilitycheck` row
Bob Merchandise is `you` and another Nathan Drake is your `partner` for a different `legalaid_eligibilitycheck` row

### legalaid_eligibilitycheck.log
As there is no way of knowing which way round entries are made in the `legalaid_personaldetails` table, this will lead to different ids being used in this table for `you_id` and `partner_id`.
This is acceptable so long as both of the ids are listed against the same `legalaid_eligibilitycheck`

### legalaid_thirdpartydetails.log
As there is no way of knowing which way round entries are made in the `legalaid_personaldetails` table, this will lead to different ids being used in this table.
This is acceptable so long as both of the ids are for a 'Nathan Drake' attached to the same `legalaid_eligibilitycheck` as Elena Fisher

### TBC


