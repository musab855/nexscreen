import sys
from unittest.mock import MagicMock

mock_st = MagicMock()
mock_st.encode.return_value = [0.1] * 384
sys.modules["sentence_transformers"] = MagicMock(SentenceTransformer=MagicMock(return_value=mock_st))