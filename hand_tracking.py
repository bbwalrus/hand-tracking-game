import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=2):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_num_hands)

    def detect_hands(self, frame, rgb_frame):
        """
        Detect hands and return the positions of the index and thumb tips.
        """
        results = self.hands.process(rgb_frame)
        hand_positions = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Capture the index finger tip (8) and thumb tip (4)
                index_tip = hand_landmarks.landmark[8]
                thumb_tip = hand_landmarks.landmark[4]

                h, w, _ = frame.shape
                # Convert normalized positions to pixel coordinates
                # Mirrored due to camera being mirrored
                index_pos = (w - int(index_tip.x * w), int(index_tip.y * h))
                thumb_pos = (w - int(thumb_tip.x * w), int(thumb_tip.y * h))

                hand_positions.append((index_pos, thumb_pos))

        return hand_positions
