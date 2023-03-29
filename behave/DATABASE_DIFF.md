## Expected Database Changes


This readme attempts to explain why there are differences between an upgrade branch and the master version of cla_backend before LGA-1773. 

If you see anything that is not explained below, then this should be queried and the document updated.

The main reasons for these changes are:
- time differences between the runs
- there is no ordering to the way in which results are stored. 
So if there is more than one row of data to add to a table, these rows can be added in a different order and so will "look" different in the target database. 

Examples are given below.


### High-level Overview
The below table shows the likely tables you will see when running the database-diff command 
with a brief explanation as to why it appears in the log. See below for a greater explanation.

| Table name                          | Reason for difference                                                    |
|-------------------------------------|--------------------------------------------------------------------------|
| cla_eventlog_log                    | (appears inconsistently) May appear if a test fails and retries          |
| cla_provider_provider_preallocation | (appears inconsistently) Test randomises this value                      |
| django_migrations                   | When explicitly adding a migration or an upgrade to a framework includes |
| django_session                      | For security purposes, the sessions renews each run                      |
| legalaid_case                       | Data is mostly the same                                                  |
| legalaid_deductions                 | Data is the same but the order they appear in the database is different  |
| legalaid_eligibilitycheck           | Data is the same but the order they appear in the database is different  |
| legalaid_income                     | Data is the same but the order they appear in the database is different  |
| legalaid_person                     | Data is the same but the order they appear in the database is different  |
| legalaid_personaldetails            | Data is the same but the order they appear in the database is different  |
| legalaid_thirdpartydetails          | Data is the same but the order they appear in the database is different  |
| summary                             | This is the high level overview/summary of the differences seen          |
| timer_timer                         | Timing difference between test runs on both branches                     |

### cla_eventlog_log.log

This may or may not appear in your runs. 
The current theory is that this only shows a difference when one of the end-to-end tests fail and auto-retries.


### cla_provider_providerpreallocation.log

Providers are allocated from a particular category. 
This is a random allocation and inconsistently appears in the database-diff logs. 
Check that the providers allocated are from the same category. 
In this case check that the `category_id` of both providers (in `cla_provider_providerallocation`) is the same. 


### django_migrations.log

This table lists all the migrations that exist and the time at which they were applied. 
As the tests are run on one branch and then the next, these application times will be different.

There could also be some new migrations when working on a new ticket.
The new migrations could either be additions you have made or could be added as part of applying an upgrade.
These should be checked and the reason for the change understood. 
You should be able to cross-reference a migration as part of an upgrade by checking the packages documentation.


### django_session.log

This table contains details of the session and this will always be different from run to run. 
Just check to make sure that there is nothing ontoward.


### legalaid_case.log

Majority of the changes are the time logged when an action has occurred on a case. 
As the tests are run against one image first before running the next, the time difference are generally 10 minutes apart.
These differences can be ignored.

provider id seems to be randomised - links to a test @complete_case / assign a case to a specialist provider
The billable time is different by a minute, this may be due to difference in timing of tests being ran
unsure what personal details link to?


### legalaid_deductions.log

In this table there are two rows that contain some `null` fields. 
The order these records are generated are random however the data generated for the table is the same.
The populated records are simply monetary values that should equate to `0` 
and payment frequency intervals that denote how often payments are made (example monthly which is recorded as `per_month`)


### legalaid_eligibilitycheck.log

As there is no way of knowing which way round entries are made in the `legalaid_personaldetails` table, 
this will lead to different ids being used in this table for `you_id` and `partner_id`.
This is acceptable so long as both of the ids are listed against the same `legalaid_eligibilitycheck`


### legalaid_income.log

The differences are similar to the legalaid_deductions table. 
The order these records are generated are random however the data generated for the table is the same.

In this table there are several rows that contain some `null` fields. 
The populated records are simply monetary values that should equate to `0` 
and payment frequency intervals that denote how often payments are made (example monthly which is recorded as `per_month`)


### legalaid_person.log

The order these records are generated is random however the data generated for the table are the same.
The legalaid_person may or may not have a `savings_id` linked to it.
Currently, we only expect to see the `savings_id` to be registered as different.


### legalaid_personaldetails.log
In the tests an eligibility check can be associated with several `legalaid_personaldetails` entries. 
It can be for `you`, your 'partner' or for a `thirdparty`. 

There is no way of knowing which order these entries will be created in the `legalaid_personaldetails` table. 
This means that they will not normally have the same id in the link tables.

Elena Fisher is `you` and a user called Nathan Drake is a `thirdparty` for a particular `legalaid_eligibilitycheck` row
Bob Merchandise is `you` and another Nathan Drake is your `partner` for a different `legalaid_eligibilitycheck` row


### legalaid_thirdpartydetails.log
As there is no way of knowing which way round entries are made in the `legalaid_personaldetails` table, 
this will lead to different ids being used in this table.
This is acceptable so long as both of the ids are for a 'Nathan Drake' attached to the same `legalaid_eligibilitycheck` as Elena Fisher


### summary.log
There will always be a summary table, use this for a high level comparison.


### timer_timer.log

This table records when the timer (which calculates how long a user has been working on a case) stops. 
These will be different because the tests are run on one branch and then the next.
