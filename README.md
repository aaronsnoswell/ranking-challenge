# Prosocial Ranking Challenge

The Prosocial Ranking Challenge is designed to inspire, fund, and test the best algorithms to improve social cohesion on social media. We will use our browser extension to re-order the feeds of paid participants on Facebook, Reddit, and X (Twitter) for three months, moving pro-social content to the top and anti-social content to the bottom, and measure changes in attitudes and behavior, including toxic polarization, dehumanization, and anti-democratic attitudes.

[More about the project here](https://link-to-website) (TODO: get link)

We are soliciting ranking algorithms to test, with a $10,000 prize for each of five winners, and $1000 for each of ten finalists.

## How to submit

Submissions will take place in two rounds: prototype and production.

### First-round: March 1, 2024

Each submission will include documentation describing how the algorithm works, what outcome(s) it is expected to change, and why it is significant to test, plus a prototype implementation (running as a live API endpoint that you host).

Ten finalists will be announced March 15, 2024. Each wins a $1000 prize.

#### First-round submission requirements

For your initial submission, you will need:

- A description of how the algorithm works, what outcome(s) it is expected to change, and why it is significant to test
- A prototype implementation. We do not need your code at this stage.
- A description of how the prototype was built, the language used, and its dependencies.
- A URL for an endpoint that hosts your algorithm, using the API specified below.

You may submit code written in any programming language or combination of languages, but we will supply example code in Python.

At this stage, it is acceptable for you to use external services, hosted models, etc.

### Finalist submissions: Apr 15, 2024

This time your ranker will need to be delivered in a Docker container, along with complete source code and build instructions. It will need to meet certain performance and security requirements.

At this point your code must be self-contained. Submissions that rely on external services will be disqualified.

Five winners will be announced May 1, 2024. Each wins a $10,000 prize, in addition to their first-round prize.

#### Finalist submission requirements

If you are selected as a finalist, you will need to provide:

- An example Docker container that runs your code, including a repeatable process for building it from source.
- A list of your external dependencies, including versions.
- Your code, so that we can perform a security audit on it.

We will rebuild your container using the audited code before running it in production. We may request your assistance during this process.

### Experiment: Jun - Oct 2024

We will test the winning rankers with real users across three different platforms for five months.

## Submitting an entry

(how to submit)

## Request/response format

NOTE: This is provisional, and will almost certainly change.

Your ranker should accept a list of social media posts, each with a corresponding ID, in JSON format:

```json
{
    "posts": [
        {
            "id": "de83fc78-d648-444e-b20d-853bf05e4f0e",
            "title": "this is the post title, available only on reddit",
            "text": "this is a social media post",
            "author_name_hash": "60b46b7370f80735a06b7aa8c4eb6bd588440816b086d5ef7355cf202a118305",
            "author_link_hash": "992c7f2cae7e746838b83ad11de1c61c798df5fd2cd8a8c7bbfb3b85650c0431",
            "type": "post",
            "platform": "reddit",
            "enagements": {
                "upvote": 34,
                "downvote": 27
            }
        }.
        {
            (etc)
        }
    ]
}
```

Your ranker should return an ordered list of IDs. You can also remove posts by removing an ID, or add posts by inserting a new ID that you generate. For new posts, the post content should be included in a separate portion of the response.

```json
{
    "ranked_ids": [
        "de83fc78-d648-444e-b20d-853bf05e4f0e",
        "571775f3-2564-4cf5-b01c-f4cb6bab461b",
        (etc)
    ],
    "new_posts": [
        {
            "id": "571775f3-2564-4cf5-b01c-f4cb6bab461b",
            "title": "this is the post title, available only on reddit",
            "text": "this is a new post to inject into the results",
            "author_name": "newguy",
            "author_link": "/u/newguy",
            "type": "post",
            "platform": "reddit",
            "enagements": {
                "upvote": 12,
                "downvote": 8
            }
        }
    ]
}
```

You do not need to return the same number of posts as you received. However, keep in mind that making a significant change in the number of posts returned could have a negative impact on the user experience.

### Platform-specific fields

Some fields are only available

## Available infrastructure

Winning classifiers will be executed in an environment that can provide the following infrastructure (let us know which you'll need):

### Endpoint

We will host your classifier endpoint. GPU is available if needed.

### Database

A database of historical post metadata for your users, updated as often as is practical, into which you can also write your own data. If needed, we can provide an interface for writing data from a process that you run outside our infrastructure, but we cannot allow that process to make queries.

### Offline Worker

A sandboxed offline worker (GPU-equipped if needed) that has read/write access to the database.

### Latency: 750ms

There is no latency requirement for initial submissions.

Finalists must finish returning their result using a standardized test set on our infrastructure within 750ms. We will test this vigorously, since latency can have an enormous impact on overall outcomes. If your classifier is too slow, we will let you know as quickly as possible, to give you time to improve your submission before the deadline.

## Security model

As this experiment handles a considerable amount of Personal Identifiable Information (PII) to which your code will have unfettered access, we must take steps to prevent data exfiltration. These will include, among other things:

- Classifiers and offline workers will be executed in a sandbox and prevented from making outgoing network connections.
- Classifier outputs will be validated.
- You will not personally have access to any user-level data about the participants in your study arm. Only aggregate data will be made available during the study. De-identified data may be made available after the study period, if it can be sufficiently de-identified.
- Our team will audit your code.

If your team needs a greater level of access to user data, that may be possible if you are working within an instution that has its own IRB and can independently review your contributions. Talk to us and we'll see if we can find a way.

## Example code

Coming soon!

In the coming weeks, we will update this git repo with an example ranker written in Python.

We will also provide a containerization example for finalist submissions.
