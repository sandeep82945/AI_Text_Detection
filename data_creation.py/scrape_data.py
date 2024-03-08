
#pip install openreview-py
import openreview

# API V2
client = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net',

    username='sandeep.kumar82945@gmail.com',
    password='marco1825'
    )

venue_id = 'EMNLP/2023/Conference'
# venue_group = client.get_group(venue_id)
# submission_name = venue_group.content['submission_name']['value']
# submissions = client.get_all_notes(invitation=f'{venue_id}/-/{submission_name}', details='replies')
submissions = client.get_all_notes(content={'venueid':venue_id} ,details='replies')

print(submissions[0].details['replies'][0])

# review_name = venue_group.content['review_name']['value']
# reviews=[openreview.api.Note.from_json(reply) for s in submissions for reply in s.details['replies'] if f'{venue_id}/{submission_name}{s.number}/-/{review_name}' in reply['invitations']]
# invitation = client.get_invitation(f'{venue_id}/-/{review_name}')
# content = invitation.edit['invitation']['edit']['note']['content']
# print(content)