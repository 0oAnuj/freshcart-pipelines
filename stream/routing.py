def topic_matches(binding: str, routing_key: str) -> bool:
    """Return whether a RabbitMQ-style topic binding matches a routing key."""
    binding_words = binding.split(".")
    key_words = routing_key.split(".")

    def match(binding_index: int, key_index: int) -> bool:
        if binding_index == len(binding_words):
            return key_index == len(key_words)

        word = binding_words[binding_index]
        if word == "#":
            return match(binding_index + 1, key_index) or (
                key_index < len(key_words)
                and match(binding_index, key_index + 1)
            )
        if key_index >= len(key_words):
            return False
        return (word == "*" or word == key_words[key_index]) and match(
            binding_index + 1, key_index + 1
        )

    return match(0, 0)
