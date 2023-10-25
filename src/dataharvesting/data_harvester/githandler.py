import git
import os


import shutil




# =======
# FEATURE:
# =======

# Pull the latest contents from remote. I need some way of determining if the local state representations the
# remote state before processing the data

# =======



# CCN:
# - Fingerprinting Technique for Youtube Videos Identification Network Traffic.


class GitHandler:
    def __init__(self, repo_name, project_dir, branch_name, uid):
        self._repo_name = repo_name
        self._tdir = project_dir + "/tmp/" + uid
        self._project_dir = project_dir + "/tmp/" + uid + "/streamingdatarepository"
        self._branch_name = branch_name
        self._repo = None
        self._branch = None

    def _clean_repo(self):
        try:
            if os.path.exists(self._tdir):
                print(f"[/]previous version detected, removing {self._tdir}.")
                # Remove directory and its contents recursively
                shutil.rmtree(self._tdir)

                # recreate temporary directory.
                os.mkdir(self._tdir)
            else:
                print(f"[/]temporary directory not found, creating {self._tdir}.")
                os.mkdir(self._tdir)

            self._repo = git.Repo.clone_from(self._repo_name, self._project_dir)
        except Exception as ex:
            print(f"Exception encountered; proceeding {ex}")

    def __enter__(self):
        try:
            self._clean_repo()
            if self._branch_name in [str(b) for b in self._repo.refs]:
                print(f"[/]Branch '{self._branch_name}' exists, skipping.")
            else:
                print(f"[+]Creating Branch: {self._branch_name}.")
                self._branch = self._repo.create_head(self._branch_name)

            self._repo.git.checkout(self._branch_name)

            if self._branch_name in self._repo.remotes:
                try:
                    print("[/]remote found, fetching.")
                    self._repo.remote(self._branch_name).fetch()
                    print("Fetched remote upstream successfully.")
                except GitCommandError as e:
                    print(f"Error fetching remote upstream: {str(e)}")
            else:
                print("Remote upstream does not exist.")

            print(f"[+]repo.init({self._project_dir})")
            self._repo.init(self._project_dir, bare=True)
        except Exception as ex:
            print(f"Exception encountered; proceeding {ex}")


    def __exit__(self, exc_type, exc_value, traceback):
        print(f"[/]exc_type:{exc_type},exc_value:{exc_value},traceback:{traceback}")

    def push_data_to_remote(self, file_paths, commit_message):
        try:
            print(f"[/] push_data_to_remote ")
            print(f"[/] {os.getcwd()} ")
            print(f"[/] file_paths:{file_paths}, commit_message:{commit_message}")
            x = self._repo.index.add(file_paths)
            y = self._repo.index.commit(commit_message)

            # =======
            # FEATURE:
            # =======
            # Proper logging of the components here required.
            # =======
            self._repo.remotes.origin.push(self._branch_name)
            self._repo.git.branch(
                "--set-upstream-to=origin/{}".format(self._branch_name), self._branch_name)
        except Exception as ex:
            print(f"Exception encountered; proceeding {ex}")

