Feature: User journeys for Fox admin or cla_backend to update the users staff status

Background: Log in to the Fox admin as a user within the super users group
    Given that I am logged in as "FOX_ADMIN_GENERAL_USER"

#Journey P11 Child 1 Navigate to users authentication page and assign user staff status (LGA-1863)
@fox-assign
Scenario: Navigate to users authentication page and assign user staff status
Given I select the link "Users"
When I select a non-staff user from the list
And I am taken to the user's details page
And I select Staff status under permissions
And I select save
Then the users details are saved and I am taken back to the list of users
And I select the link "Log out"

#Journey P11 Child 2, Child 3 Create an operator user and login (LGA-1864, LGA-1865)
@fox-create-user
Scenario: Create an operator user
Given I select the link "Operators"
And I choose to "Add operator"
And I am taken to the "Add operator" page located on "/admin/call_centre/operator/add/"
And I create a new operator user
And I select 'Is active’
And I choose to "save"
Then the new operator user is created
And I am taken to the list of operators page
And I select the link "Log out"
And that I am logged in as "FOX_ADMIN_NEW_USER"