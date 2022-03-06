import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# Authentication
auth = HTTPBasicAuth('vasikyrg', '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')
# auth = HTTPBasicAuth('DimitriosSpanos', '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')


# Get info about a specific user/organization by his/her/its username
def get_user(username):
    url = "https://api.github.com/users/" + username
    r = requests.get(url=url, params={}, auth=auth)
    response = r.json()
    # print(response["repos_url"])
    return response


def get_organization(username):
    url = "https://api.github.com/orgs/" + username
    r = requests.get(url=url, params={}, auth=auth)
    response = r.json()
    # print(response["repos_url"])
    return response


# Get the public repositories of a user/organization
def get_user_repos(username):
    url = "https://api.github.com/users/" + username + "/repos"
    r = requests.get(url=url, params={}, auth=auth)
    response = r.json()
    # print(response[0].keys())
    # for repo in response:
    #     #     print(repo["name"])
    #         print(repo["language"])
    return response


# Get the information of a public repository
def get_repo_info(repoOwner, repoName):
    url = "https://api.github.com/repos/" + repoOwner + "/" + repoName
    r = requests.get(url=url, params={}, auth=auth)
    response = r.json()
    print(response)
    return response


# Get basic information about the most popular repositories
def get_most_popular_repositories_info():
    repos = pd.read_csv("./mostPopularRepositories.csv", sep=";")
    for _, row in repos.iterrows():
        url = "https://api.github.com/repos/" + row.RepositoryOwner + "/" + row.RepositoryName
        r = requests.get(url=url, params={}, auth=auth)
        response = r.json()
        print(response)
        if "topics" in response:
            print(response["topics"])
        return response


# Get the comments in issues of a public repository
def get_repo_issues_comments(repoOwner, repoName):
    url = "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/issues/comments"
    r = requests.get(url=url, params={}, auth=auth)
    response = r.json()
    print(response)
    return response


# Get the releases of a public repository
def get_repo_releases(repoOwner, repoName):
    url = "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/releases"
    r = requests.get(url=url, params={}, auth=auth)
    response = r.json()
    print(response)
    return response


# Get a specific commit of a public repository
def get_repo_commit(repoOwner, repoName, commitSHA):
    url = "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/commits/" + commitSHA
    r = requests.get(url=url, params={}, auth=auth)
    response = r.json()
    print(response)
    return response


# MY FUNCTIONS

def organization_info(organization):
    print("Name: {}".format(get_organization(organization)['name']))
    print("Email: {}".format(get_organization(organization)['email']))
    print("Location: {}".format(get_organization(organization)['location']))
    print("Public repos: {}".format(get_organization(organization)['public_repos']))
    print("members_url: {}".format(get_organization(organization)['members_url']))
    print("Description: {}".format(get_organization(organization)['description']))
    print("Has organization projects ?: {}".format(get_organization(organization)['has_organization_projects']))


def most_common(lst):
    users_most_used_language = []
    response = get_user_repos(lst)
    for repo in response:
        if repo["language"] != None:
            users_most_used_language.append(repo["language"])
    if users_most_used_language:
        most_com = max(users_most_used_language, key=users_most_used_language.count)
    else:
        most_com = 'No repos'
    # print("\nMost Common Language of " + str(lst) + " : " + str(most_com))
    return most_com


def get_members(organization):
    members = []
    members_url = "https://api.github.com/orgs/" + organization + "/members"
    r = requests.get(url=members_url, params={}, auth=auth)
    response = r.json()
    # token_prob = []
    # count = 0
    while 'next' in r.links.keys():
        r = requests.get(r.links['next']['url'], auth=auth)
        response.extend(r.json())
        # count = count+1
        # print("\nPage = "+str(count))
    for repo in range(0, 15):
        # counter = counter + 1
        # print("\nusername: {}".format(repo['login']))
        # print("Full Name: {}".format(getUser(repo['login'])['name']))
        members.append(response[repo]['login'])
    # print("Members of "+str(getOrganization(organization)['name']+" are "+str(counter)))
    # for mem in range(70, 80):
    #     token_prob.append(members[mem])

    return members


def get_member_list(members, organization):
    member_list = []
    counter = 0
    total_stars = repos_stars(members)
    total_forks = get_forks(members)
    total_commits = get_commits(members)
    watchers_per_repo = get_watchers(members)
    total_open_issues, total_closed_issues = issues(members)
    licenses_percentage = licenses(members)
    for member in range(0, len(members)):
        # print("\nName: {}".format(getUser(channel)['name']))
        # print("Company: {}".format(getUser(channel)['company']))
        # print("Location: {}".format(getUser(channel)['location']))
        # print("Blog: {}".format(getUser(channel)['blog']))
        # print("Public repos: {}".format(getUser(channel)['public_repos']))
        # print("Followers: {}".format(getUser(channel)['followers']))
        # print("Following: {}".format(getUser(channel)['following']))
        # print("About: {}".format(getUser(channel)['bio']))
        most_com = most_common(members[member])
        stars = total_stars[member]
        forks = total_forks[member]
        commits = total_commits[member]
        watchers = watchers_per_repo[member]
        open_issues = total_open_issues[member]
        closed_issues = total_closed_issues[member]
        license = licenses_percentage[member]
        if 'error' not in members[member]:
            member_list.append(
                [members[member], organization, get_user(members[member])['public_repos'],
                 get_user(members[member])['followers'], get_user(members[member])['following'], most_com, stars,
                 forks, commits, watchers, license, open_issues, closed_issues])
            counter = counter + 1
            print("\nUser " + str(members[member]) + " has been entered, number: " + str(counter))
    return member_list


def create_dataset(member_list):
    dataset = pd.DataFrame(member_list)
    dataset.columns = ['Username', 'Company', 'Public Repositories', 'Followers', 'Following',
                       'Most Common Language', 'Total Stars', 'Total Forks', 'Commits', 'Watchers/Repo',
                       'Licenses(%)', 'Open Issues', 'Closed Issues']

    dataset.to_csv('dataset.csv', index=False)


def repos_stars(members):
    url_data = []
    total_stars_repo = []
    stars_array = []
    for member in range(0, len(members)):
        # total_stars = []
        url_data.append(get_user(members[member])["repos_url"])
        url = url_data[member]
        r = requests.get(url=url, params={}, auth=auth)
        response = r.json()
        if 'next' in r.links.keys():
            while 'next' in r.links.keys():
                r = requests.get(r.links['next']['url'], auth=auth)
                response.extend(r.json())
            for repo in range(0, len(response)):
                stars_array.append(response[repo]['stargazers_count'])
                # print(response[repo]['name']+" has "+str(stars_array[repo])+" stars.")
        else:
            for repo in range(0, len(response)):
                stars_array.append(response[repo]['stargazers_count'])
                # print(response[repo]['name'] + " has " + str(stars_array[repo]) + " stars.")
        total_stars_repo.append(sum(stars_array))
        # print(response['name'] + " has " + str(total_stars_repo[member]) + " total stars.")
        # total_stars.append(sum(total_stars_repo))
        # print("User " + str(members[member]) + " TOTAL STARS are: "+str(total_stars_repo[member]))
        stars_array.clear()
    return total_stars_repo


def get_forks(members):
    url_data = []
    total_forks_repo = []
    forks_array = []
    for member in range(0, len(members)):
        url_data.append(get_user(members[member])["repos_url"])
        url = url_data[member]
        r = requests.get(url=url, params={}, auth=auth)
        response = r.json()
        # counter = 0
        if 'next' in r.links.keys():
            while 'next' in r.links.keys():
                r = requests.get(r.links['next']['url'], auth=auth)
                response.extend(r.json())
            for repo in range(0, len(response)):
                if not response[repo]['fork']:
                    # print(response[repo]['fork'])
                    forks_array.append(response[repo]['forks_count'])
                    # print("\n"+response[repo]['name']+" has "+str(forks_array[counter])+" forks.")
                    # counter = counter+1
        else:
            for repo in range(0, len(response)):
                if not response[repo]['fork']:
                    forks_array.append(response[repo]['forks_count'])
                    # print(response[repo]['name'] + " has " + str(forks_array[repo]) + " forks.")
        total_forks_repo.append(sum(forks_array))
        # print("User " + str(members[member]) + " TOTAL FORKS are: "+str(total_forks_repo[member]))
        forks_array.clear()
    return total_forks_repo


def get_commits(members):
    url_data = []
    total_commits_array = []
    commits_array = []
    for member in range(0, len(members)):
        url_data.append(get_user(members[member])["repos_url"])
        url = url_data[member]
        r = requests.get(url=url, params={}, auth=auth)
        response = r.json()
        if 'next' in r.links.keys():
            while 'next' in r.links.keys():
                r = requests.get(r.links['next']['url'], auth=auth)
                response.extend(r.json())
            for repo in range(0, len(response)):
                if not response[repo]['fork']:
                    url = response[repo]['commits_url'].split("{")[0]
                    re = requests.get(url=url, params={}, auth=auth)
                    res = re.json()
                    if 'next' in re.links.keys():
                        while 'next' in re.links.keys():
                            re = requests.get(re.links['next']['url'], auth=auth)
                            res.extend(re.json())
                        # print("URL: {}, commits: {}".format(url, len(res)))
                        commits_array.append(len(res))
                    else:
                        if not response[repo]['fork']:
                            # print("URL: {}, commits: {}".format(url, len(res)))
                            commits_array.append(len(res))
        else:
            for repo in range(0, len(response)):
                if not response[repo]['fork']:
                    url = response[repo]['commits_url'].split("{")[0]
                    re = requests.get(url=url, params={}, auth=auth)
                    res = re.json()
                    if 'next' in re.links.keys():
                        while 'next' in re.links.keys():
                            re = requests.get(re.links['next']['url'], auth=auth)
                            res.extend(re.json())
                        # print("URL: {}, commits: {}".format(url, len(res)))
                        commits_array.append(len(res))
                    else:
                        if not response[repo]['fork']:
                            # print("URL: {}, commits: {}".format(url, len(res)))
                            commits_array.append(len(res))
        total_commits_array.append(sum(commits_array))
        print("User " + str(members[member]) + " TOTAL commits are: "+str(total_commits_array[member]))
        commits_array.clear()
    return total_commits_array


def get_watchers(members):
    url_data = []
    total_watchers_array = []
    watchers_array = []
    watchers_per_repo = []
    for member in range(0, len(members)):
        url_data.append(get_user(members[member])["repos_url"])
        url = url_data[member]
        r = requests.get(url=url, params={}, auth=auth)
        response = r.json()
        if 'next' in r.links.keys():
            while 'next' in r.links.keys():
                r = requests.get(r.links['next']['url'], auth=auth)
                response.extend(r.json())
            for repo in range(0, len(response)):
                if not response[repo]['fork']:
                    url = response[repo]['subscribers_url'].split("{")[0]
                    re = requests.get(url=url, params={}, auth=auth)
                    res = re.json()
                    if 'next' in re.links.keys():
                        while 'next' in re.links.keys():
                            re = requests.get(re.links['next']['url'], auth=auth)
                            res.extend(re.json())
                        # print("URL: {}, watchers: {}".format(url, len(res)))
                        watchers_array.append(len(res))
                    else:
                        if not response[repo]['fork']:
                            # print("URL: {}, watchers: {}".format(url, len(res)))
                            watchers_array.append(len(res))
        else:
            for repo in range(0, len(response)):
                if not response[repo]['fork']:
                    url = response[repo]['subscribers_url'].split("{")[0]
                    re = requests.get(url=url, params={}, auth=auth)
                    res = re.json()
                    if 'next' in re.links.keys():
                        while 'next' in re.links.keys():
                            re = requests.get(re.links['next']['url'], auth=auth)
                            res.extend(re.json())
                        # print("URL: {}, watchers: {}".format(url, len(res)))
                        watchers_array.append(len(res))
                    else:
                        if not response[repo]['fork']:
                            # print("URL: {}, watchers: {}".format(url, len(res)))
                            watchers_array.append(len(res))
        total_watchers_array.append(sum(watchers_array))
        if total_watchers_array[member] == 0:
            watchers_per_repo.append(total_watchers_array[member])
        else:
            watchers_per_repo.append(total_watchers_array[member] / (len(watchers_array)))
        # print("User " + str(members[member]) + " TOTAL watchers are: " + str(total_watchers_array[member]))
        # print("User " + str(members[member]) + " has " + str(watchers_per_repo[member]) + " watchers/repo")
        watchers_array.clear()
    return watchers_per_repo


def licenses(members):
    url_data = []
    total_licenses_repo = []
    licenses_array = []
    licenses_percentage = []
    # counter = 0
    for member in range(0, len(members)):
        # total_stars = []
        url_data.append(get_user(members[member])["repos_url"])
        url = url_data[member]
        r = requests.get(url=url, params={}, auth=auth)
        response = r.json()
        if 'next' in r.links.keys():
            while 'next' in r.links.keys():
                r = requests.get(r.links['next']['url'], auth=auth)
                response.extend(r.json())
            for repo in range(0, len(response)):
                if not response[repo]['fork']:
                    licenses_array.append(1 if response[repo]['license'] != None else 0)
                    # print(response[repo]['name']+" has "+str(response[repo]['license']['name']
                    #                                          if response[repo]['license'] != None else 0)+" license.")
                    # counter = counter + 1
        else:
            for repo in range(0, len(response)):
                if not response[repo]['fork']:
                    licenses_array.append(1 if response[repo]['license'] != None else 0)
                    # print(response[repo]['name'] + " has " + str(response[repo]['license']['name']
                    #                                              if response[repo]['license'] != None else 0) + " license.")
                    # counter = counter + 1
        total_licenses_repo.append(sum(licenses_array))
        if total_licenses_repo[member] == 0:
            licenses_percentage.append(total_licenses_repo[member])
        else:
            licenses_percentage.append(total_licenses_repo[member] / (len(licenses_array)))
        # print("User " + str(members[member]) + " TOTAL licenses are: " + str(total_licenses_repo[member]))
        # print("User " + str(members[member]) + " has " + str(licenses_percentage[member]) + " % licenses")
        licenses_array.clear()
    return licenses_percentage


def issues(members):
    states = ["closed", "open"]
    extra = "/pulls?state="
    url_data = []
    open_issues = []
    total_open_issues = []
    closed_issues = []
    total_closed_issues = []
    counter = 0
    for member in range(0, len(members)):
        url_data.append(get_user(members[member])["repos_url"])
        url = url_data[member]
        r = requests.get(url=url, params={}, auth=auth)
        response = r.json()
        if 'next' in r.links.keys():
            while 'next' in r.links.keys():
                r = requests.get(r.links['next']['url'], auth=auth)
                response.extend(r.json())
                for repo in range(0, len(response)):
                    if not response[repo]['fork']:
                        url_n = response[repo]['url'] + extra
                        for state in states:
                            url = url_n + state
                            re = requests.get(url=url, params={}, auth=auth)
                            res = re.json()
                            if 'next' in re.links.keys():
                                while 'next' in re.links.keys():
                                    re = requests.get(re.links['next']['url'], auth=auth)
                                    res.extend(re.json())
                            if state == "open":
                                # print("URL: {}, {} issues: {}".format(url, state, len(res)))
                                open_issues.append(len(res))
                            else:
                                # print("URL: {}, {} issues: {}".format(url, state, len(res)))
                                closed_issues.append(len(res))
        else:
            for repo in range(0, len(response)):
                if not response[repo]['fork']:
                    url_n = response[repo]['url'] + extra
                    for state in states:
                        url = url_n + state
                        re = requests.get(url=url, params={}, auth=auth)
                        res = re.json()
                        if 'next' in re.links.keys():
                            while 'next' in re.links.keys():
                                re = requests.get(re.links['next']['url'], auth=auth)
                                res.extend(re.json())
                        if state == "open":
                            # print("URL: {}, {} issues: {}".format(url, state, len(res)))
                            open_issues.append(len(res))
                        else:
                            # print("URL: {}, {} issues: {}".format(url, state, len(res)))
                            closed_issues.append(len(res))
        total_open_issues.append(sum(open_issues))
        total_closed_issues.append(sum(closed_issues))
        # print("User " + str(members[member]) + " open issues are: " + str(total_open_issues[member]))
        # print("User " + str(members[member]) + " closed issues are: " + str(total_closed_issues[member]))
        counter = counter + 1
        # print("\nUser " + str(members[member]) + " has been entered, number: " + str(counter))
        closed_issues.clear()
        open_issues.clear()
    return total_open_issues, total_closed_issues


def main():
    org = "ros"
    members = get_members(org)
    member_list = get_member_list(members, org)
    create_dataset(member_list)
    # commits = get_commits(members)
    # organization_info(org)
    # dataset_commits = pd.DataFrame(members, columns=['Username'])
    # dataset_members.to_csv('dataset_members.csv', index=False)
    # members_list = get_member_list(org)
    # create_dataset(members_list)
    # total_open_issues, total_closed_issues = issues(org)
    # dataset_commits["Commits"] = commits
    # dataset_mercedes["Closed Issues"] = total_closed_issues
    # dataset_commits.to_csv('dataset_commits.csv')


if __name__ == '__main__':
    main()

# getUser("AuthEceSofteng")
# getUserRepos("AuthEceSofteng")
# getRepoInfo("AuthEceSofteng", "emb-ntua-workshop")
# getMostPopularRepositoriesInfos()
# getRepoIssuesComments("AuthEceSofteng", "emb-ntua-workshop")
# getRepoReleases("AuthEceSofteng", "emb-ntua-workshop")
# getRepoCommit("AuthEceSofteng", "emb-ntua-workshop", "41e03e26db38caf3d2b9c500d56be1a1327d8c84")
