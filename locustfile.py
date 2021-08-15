from locust import HttpUser, task, between
import server


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        """"""
        self.client.get("/")

    @task
    def login(self):
        """"""
        self.client.post("/showSummary",
                         data={"email": "admin@irontemple.com"})

    @task
    def competitions(self):
        """"""
        for competitions in server.competitions:
            for clubs in server.clubs:
                fstring = f"/book/{competitions['name']}/{clubs['name']}"
                self.client.get(fstring)

    @task
    def buy(self):
        """"""
        for competitions in server.competitions:
            for clubs in server.clubs:
                club = clubs['name']
                competition = competitions['name']
                self.client.post('/purchasePlaces',
                                 data={'club': club,
                                       'competition': competition,
                                       'places': '1'})
