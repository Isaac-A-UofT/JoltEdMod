from tutorials_generator.block import Block, SeedBlock, ExplanatoryBlock, KnowledgeTestingBlock, CurriculumBlock

class BlockFactory:
    BLOCK_TYPES = {
        'SeedBlock': SeedBlock,
        'ExplanatoryBlock': ExplanatoryBlock,
        'KnowledgeTestingBlock': KnowledgeTestingBlock,
        'CurriculumBlock': CurriculumBlock,
    }
    
    @staticmethod
    def create_block(block_config):
        block_type = block_config['type']
        block_class = BlockFactory.BLOCK_TYPES.get(block_type)
        if not block_class:
            raise ValueError(f"Invalid block type: {block_type}")
        return block_class(**block_config)
