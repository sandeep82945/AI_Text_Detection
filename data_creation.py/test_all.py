#pip install openreview-py
import openreview
import json

# API V2
client = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net',
    username='sandeep.kumar82945@gmail.com',
    password='marco1825'
)

venue_id = 'EMNLP/2023/Conference'
submissions = client.get_all_notes(content={'venueid': venue_id}, details='replies')

# Create a list to store data
review_data = []

# Retrieve the first submission
# first_submission = submissions[0] if submissions else None

for submission in submissions:
  if submission:
      paper_link = submission.content.get('pdf', '')
      
      # Get official reviews for the first submission
      official_reviews = submission.details.get('replies', [])

      # Store the paper link and reviews in the list
      paper_data = {'Paper Link': paper_link, 'Reviews': []}
      for i, review in enumerate(official_reviews, start=1):
          if 'content' in review:
            if 'rebuttal' not in review['content'] and 'acknowledgement' not in review['content'] and 'metareview' not in review['content']:
              if 'decision' not in review['content']:
                paper_data['Reviews'].append({f'Review {i} Content': review['content']})
              else:
                paper_data['Reviews'].append({'Paper Decision': review['content']})

      # Append the paper data to the review_data list
      review_data.append(paper_data)

      # Write the data to a JSON file
      json_filename = 'paper_reviews_all.json'
      with open(json_filename, 'w', encoding='utf-8') as json_file:
          json.dump(review_data, json_file, ensure_ascii=False, indent=2)

      print(f"Data has been stored in {json_filename}")
  else:
      print("No submissions found.")