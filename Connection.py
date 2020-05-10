import krpc

class Connection:
    conn=None

    def get_conn(self, name=None, ip=None, ports=None):
        if self.conn is None:
            self.conn = krpc.connect(name, ip, ports[0], ports[1])

        return self.conn