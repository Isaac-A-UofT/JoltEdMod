from jolted_mod.block import (
    Block,
    SeedBlock,
    ExplanatoryBlock,
    KnowledgeTestingBlock,
)


class BlockFactory:
    BLOCK_TYPES = {
        "SEED_BLOCK": SeedBlock,
        "EXPLANATORY_BLOCK": ExplanatoryBlock,
        "KNOWLEDGE_TESTING_BLOCK": KnowledgeTestingBlock,
    }

    @staticmethod
    def create_block(block_config: dict) -> Block:
        block_type = block_config["type"]
        block_class = BlockFactory.BLOCK_TYPES.get(block_type)
        if not block_class:
            raise ValueError(f"Invalid block type: {block_type}")
        return block_class(**block_config)
