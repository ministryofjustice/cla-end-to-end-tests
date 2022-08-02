Feature: User journeys for Fox admin or cla_backend to update the users staff status

Background: Log in to the Fox admin as a user within the super users group
    Given that I am logged in as "FOX_ADMIN_GENERAL_USER"

#Journey P11  Navigate to users authentication page and assign user staff status (LGA-1863)
@fox-assign
Scenario: Navigate to users authentication page and assign user staff status
Given I select the link "Users"
When I select a non-staff user from the list
And I am taken to the user's details page
And I select Staff status under permissions
And I select save
Then the users details are saved and I am taken back to the list of users
And I select the link "Log out"