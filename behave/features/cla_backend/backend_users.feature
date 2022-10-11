Feature: User journeys for Fox admin or cla_backend to update the users staff status

Background: Log in to the Fox admin as a user within the super users group
    Given I am logged in as "FOX_ADMIN_GENERAL_USER"

#Journey P11 Child 1 Navigate to users authentication page and assign user staff status (LGA-1863)
@fox-assign
Scenario: Navigate to users authentication page and assign user staff status
Given I select the link "Users"
When I select a non-staff user from the list
And I am taken to the non-staff user's details page
And I select Staff status under permissions
And I select save
Then the users details are saved and I am taken back to the list of users
And I select the link "Log out"

#Journey P11 Child 2, Child 3, Child 4, Create an operator user, login CHS with new user then delete user
# (LGA-1864, LGA-1865, LGA-1866)
@fox-create-user
Scenario: Create an operator user
Given I select the link "Operators"
And I choose to "Add operator"
And I am taken to the "Add operator" page located on "/admin/call_centre/operator/add/"
And I create a new operator user
And I select 'Is active'
And I choose to "save"
Then the new operator user is created
And I am taken to the list of operators page
#Child 3
And I select the link "Log out"
And I am logged in as "NEWLY_CREATED_OPERATOR"
Then I am on the 'call centre dashboard' page
#Child 4
And I am logged in as "FOX_ADMIN_GENERAL_USER"
And I select the link "Users"
And I select the newly created user from the list
And I am taken to the user's details page
When I select 'Delete' in the user's details page
Then I am taken to the 'Are you sure page'
And I select the 'Yes, I'm sure'
Then I confirm the user has been deleted from the list of users
