class MessageSystem:
    def __init__(self):
        self.messages = []

    def write_message(self, message: str):
        """Ajouter un message à la liste des messages"""
        self.messages.append(message)
        print(f"Message écrit: {message}")

    def receive_messages(self):
        """Recevoir tous les messages et les supprimer de la liste"""
        if not self.messages:
            print("Aucun message à recevoir.")
            return []
        
        received = self.messages[:]
        
        self.messages.clear()
        
        print("Messages reçus:", received)
        return received



def test_message_system():
    system = MessageSystem()
    
    system.write_message("Bonjour, comment ça va ?")
    system.write_message("Ca va et toi mon pote .")
    system.write_message("C'est un test pour voir si tout rouler.")
    
    messages = system.receive_messages()
    
    assert len(system.messages) == 0, "Les messages n'ont pas été supprimés après réception."
    
    no_messages = system.receive_messages()
    assert len(no_messages) == 0, "Il y a encore des messages après réception."
    
    system.write_message("Un nouveau message.")
    new_message = system.receive_messages()
    assert new_message == ["Un nouveau message."], "Le dernier message n'a pas été correctement reçu."

test_message_system()
